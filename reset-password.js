const admin = require('firebase-admin');
const serviceAccount = require('./serviceAccountKey.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

// Aapka User ID
const uid = 'muYSLFjaleWi6PN2Tyf9fOXbksk1';
// Aapka naya password
const newPassword = 'alibaba6631720@@';

admin.auth().updateUser(uid, {
  password: newPassword
}).then((userRecord) => {
  console.log('✅ Password successfully change ho gaya!');
  console.log('Naya Password:', newPassword);
}).catch((error) => {
  console.log('❌ Error aya:', error.message);
});
