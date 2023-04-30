// this file performs operations relating to the firestore database

import firebase from 'firebase/app/dist/index.cjs.js';
import 'firebase/firestore/dist/index.node.cjs.js';

// pull in env vars
const apiKeyVal = process.env.apiKey;
const authDomainVal = process.env.authDomain;
const projectIdVal = process.env.projectId;
const storageBucketVal = process.env.storageBucket;
const messagingSenderIdVal = process.env.messagingSenderId;
const appIdVal = process.env.appId;

// Firebase project configuration
const firebaseConfig = {
    apiKey: apiKeyVal,
    authDomain: authDomainVal,
    projectId: projectIdVal,
    storageBucket: storageBucketVal,
    messagingSenderId: messagingSenderIdVal,
    appId: appIdVal
    };

// initialize db
firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

// retrieve jobs from the database
export async function getAllJobs() {
    try {
        const querySnapshot = await db.collection('web3-remote-jobs').get();
        const jobs = [];
        
        querySnapshot.forEach((doc) => {
            const { company, dateAdded, jobTitle, url } = doc.data();
            
            const thirtyOneDaysAgo = new Date();
            thirtyOneDaysAgo.setDate(thirtyOneDaysAgo.getDate() - 31);
            
            if (dateAdded.toDate() > thirtyOneDaysAgo) {
            jobs.push({ company, dateAdded, jobTitle, url });
            }
        });
    
        return jobs;
        } catch (e) {
        console.error('Error retrieving jobs from database: ', e);
        return [];
        }
    }
