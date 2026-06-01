const { initializeApp } = require('firebase/app');
const { getFirestore, collection, getDocs, query, orderBy, limit } = require('firebase/firestore');

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

async function checkLeads() {
  console.log("Fetching latest leads...");
  const leadsRef = collection(db, 'leads');
  const q = query(leadsRef, orderBy('createdAt', 'desc'), limit(15));
  const querySnapshot = await getDocs(q);
  console.log("Total leads retrieved:", querySnapshot.size);
  querySnapshot.forEach((doc) => {
    const data = doc.data();
    console.log(`- ID: ${doc.id}`);
    console.log(`  Name: ${data.name}`);
    console.log(`  Company: ${data.company}`);
    console.log(`  Email: ${data.email}`);
    console.log(`  Phone: ${data.phone}`);
    console.log(`  CreatedAt: ${data.createdAt}`);
  });
}

checkLeads().catch(console.error);
