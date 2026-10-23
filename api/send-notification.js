const admin = require('firebase-admin');

// Load service account key
// On Vercel, we will use Environment Variables for security
let serviceAccount;
try {
  // For local testing, try to read the file
  serviceAccount = require('../serviceAccountKey.json');
} catch (error) {
  // For Vercel deployment, read from Environment Variable
  if (process.env.FIREBASE_SERVICE_ACCOUNT) {
    serviceAccount = JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT);
  } else {
    console.error("Service account key not found.");
  }
}

if (serviceAccount && !admin.apps.length) {
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
  });
}

module.exports = async (req, res) => {
  // Enable CORS so our website can call this API
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'OPTIONS,POST');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { token, title, body } = req.body;

  if (!token || !title || !body) {
    return res.status(400).json({ error: 'Missing required fields: token, title, body' });
  }

  try {
    const message = {
      notification: { title, body },
      token: token,
      webpush: {
        fcmOptions: {
          link: 'https://beinghumanblood.vercel.app/?openRequests=true'
        }
      }
    };

    const response = await admin.messaging().send(message);
    res.status(200).json({ success: true, response });
  } catch (error) {
    console.error('Error sending message:', error);
    res.status(500).json({ success: false, error: error.message });
  }
};
