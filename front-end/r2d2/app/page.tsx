'use client'
import { useState, useEffect, FormEvent } from 'react'
import styles from './page.module.css'
import Research from './research';

export default function Home() {

  // fetches List of competitors and research on each competitors
  const handleCompetitorResearch = async () => {
    const res = await fetch("http://localhost:8000/competitors", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({"industry": industry})
    });

    const data = await res.json();
    setData(data.message);
    setLoading(false);
    setLoadData(true);

    //const data = await res.json();
  }

  // fetches email sequences
  const handlePersonalizedEmail = async () => {
      const res = await fetch("http://localhost:8000/email", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({"name": name})
      });

      const data = await res.json();
      setEmails(data.message);
  }

  const [industry, setIndustry] = useState("");
  const [loading, setLoading] = useState(false);
  const [loadData, setLoadData] = useState(false);
  const [data, setData] = useState([]);
  const [name, setName] = useState("");
  const [emails, setEmails] = useState("");

  return (
    <main className={styles.main}>
      <div>
        <h2>Hello, Welcome to my R2D2 Assessment</h2>
        <h2>Competitor Research</h2>
        <form onSubmit={(e) => {
          e.preventDefault();
          setLoading(true);
          handleCompetitorResearch();
        }}>
          <label htmlFor="">I want to find a list of competitors within this industry:</label>
          <input type="text" name="industry" placeholder='Enter industry' value={industry} onChange={(e) => setIndustry(e.target.value)}/>
          <button type="submit">Search Competitors</button>
        </form>
        { loading && (<div>Loading...</div>)}
        { loadData && data.map((data, id) => <Research key={id} props={data}></Research>)}
      </div>
      <div>
        <h2>Personalized Emails</h2>
        <form onSubmit={(e) => {
          e.preventDefault();
          handlePersonalizedEmail();
        }}>
          <label>Write up a personalized email outreach towards someone named: </label>
          <input type="text" name="name" placeholder='Enter Name' value={name} onChange={(e) => setName(e.target.value)}/>
          <button type="submit">Get Email</button>
        </form>
        <div>
          { emails != "" && (<p>{emails}</p>)}
        </div>
      </div>
    </main>
  )
}
