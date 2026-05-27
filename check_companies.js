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
  const querySnapshot = await getDocs(collection(db, 'companies'));
  querySnapshot.forEach((doc) => {
    const data = doc.data();
    console.log(`- ID: ${doc.id}, name: ${data.name}, loginCode: ${data.loginCode}`);
  });
}

check().catch(console.error);
