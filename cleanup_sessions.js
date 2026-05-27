const { initializeApp } = require('firebase/app');
const { getFirestore, collection, getDocs, doc, updateDoc, addDoc, serverTimestamp } = require('firebase/firestore');

const firebaseConfig = {
  apiKey: 'AIzaSyD8bNj7KimdgkZ8rKyd4DACwHWGtbFBpTM',
  authDomain: 'onstaffai.firebaseapp.com',
  projectId: 'onstaffai',
  storageBucket: 'onstaffai.firebasestorage.app',
  messagingSenderId: '928687174326',
  appId: '1:928687174326:web:859a3cc6719843457dec17'
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

async function cleanup() {
  const querySnapshot = await getDocs(collection(db, 'agentSessions'));
  const now = new Date();
  
  let count = 0;

  for (const sessionDoc of querySnapshot.docs) {
    const data = sessionDoc.data();
    if (data.status === 'closed') continue;

    let lastUpdate = data.lastUpdate;
    if (!lastUpdate) {
        lastUpdate = data.sessionStart;
    }
    
    if (lastUpdate && typeof lastUpdate.toDate === 'function') {
        lastUpdate = lastUpdate.toDate();
    } else if (typeof lastUpdate === 'string') {
        lastUpdate = new Date(lastUpdate);
    } else if (lastUpdate && lastUpdate.seconds) {
        lastUpdate = new Date(lastUpdate.seconds * 1000);
    } else {
        continue;
    }

    const diffHours = (now.getTime() - lastUpdate.getTime()) / (1000 * 60 * 60);

    if (diffHours >= 24) {
        console.log(`Closing session ${sessionDoc.id} (inactive for ${Math.round(diffHours)} hours)`);
        
        // Add message
        await addDoc(collection(db, `agentMessages/${sessionDoc.id}/messages`), {
            text: "השיחה הסתיימה מחוסר תגובה",
            sender: "agent",
            ts: serverTimestamp()
        });

        // Update session
        await updateDoc(doc(db, 'agentSessions', sessionDoc.id), {
            status: 'closed',
            lastUpdate: serverTimestamp(),
            lastUserMsg: "השיחה הסתיימה מחוסר תגובה",
            unread: false
        });
        
        count++;
    }
  }
  
  console.log(`Successfully closed ${count} inactive sessions.`);
  process.exit(0);
}

cleanup().catch(e => {
    console.error(e);
    process.exit(1);
});
