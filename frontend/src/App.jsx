import './App.css'
import { useState } from "react";

import Submit_button from './components/submit_button'
import Heading from './components/Heading'
import Progress from './components/Progress'




export default function App() {
  const [file, setFile] = useState(null);

  async function uploadVideo() {
    if(!file) {
      alert("Please select a video first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try{
      const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      console.log(data);
      alert("Upload successful!");
    } catch (error) {
      console.error(error);
      alert("Upload failed.");
    }
  }


  return(
    <div className='app-container'>
      <Heading></Heading>
      <input type='file' accept='video/*'
        onChange={
          (e) => setFile(e.target.files[0])
        }
      />
      <Submit_button onClick={uploadVideo}></Submit_button>
      <Progress></Progress>
    </div>
  )
}