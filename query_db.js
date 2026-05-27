const { initializeApp } = require('firebase/app');
const { getFirestore, collection, getDocs } = require('firebase/firestore');

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

async function check() {
  const querySnapshot = await getDocs(collection(db, 'agentSessions'));
  console.log("Total sessions:", querySnapshot.size);
  querySnapshot.forEach((doc) => {
    const data = doc.data();
    console.log(`- ID: ${doc.id}, clientKey: ${data.clientKey}, status: ${data.status}`);
  });
}

check().catch(console.error);
