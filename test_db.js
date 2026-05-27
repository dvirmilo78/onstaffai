const { initializeApp } = require('firebase/app');
const { getFirestore, collection, getDocs } = require('firebase/firestore');

const firebaseConfig = {
  projectId: "onstaffai",
  // add minimum config to connect, but I need the API key!
};
// I can extract the config from their client_portal.html!
