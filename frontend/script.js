import {data} from "../data/data.js";

const classSelect = document.getElementById("classSelect");
const subjectSelect = document.getElementById("subjectSelect");
const chapterSelect = document.getElementById("chapterSelect");

// 1. When Class changes, update Subjects
classSelect.onchange = function() {
  subjectSelect.length = 1; // Reset
  chapterSelect.length = 1; // Reset
  
  const subjects = data[this.value];
  if (subjects) {
    for (let sub in subjects) {
      subjectSelect.add(new Option(sub, sub));
    }
  }
};

// 2. When Subject changes, update Chapters
subjectSelect.onchange = function() {
  chapterSelect.length = 1; // Reset
  
  const selectedClass = classSelect.value;
  const chapters = data[selectedClass][this.value];
  
  if (chapters) {
    chapters.forEach(chap => {
      chapterSelect.add(new Option(chap, chap));
    });
  }
};









// const api_key = "AIzaSyC1-EQwFTWeuWUBsb_-0i4A5dUjgA23Ufc"

// let topic = 'Projectile Motion HSC Problem Solving'

// async function getBestVideo(topic) {
//     const api_key = "AIzaSyC1-EQwFTWeuWUBsb_-0i4A5dUjgA23Ufc"
//     const searchUrl = `https://www.googleapis.com/youtube/v3/search?part=snippet&q=${encodeURIComponent(topic)}&type=video&maxResults=20&key=${api_key}`;
    
//     const response = await fetch(searchUrl);
//     const data = await response.json();

//     const allIds = data.items.map(item => item.id.videoId).join(',');

//     const stats = await getVideoList(allIds)
//     stats.items.forEach(video => {
//         if (video.statistics.viewCount > 1000) {
//             console.log(`https://www.youtube.com/watch?v=${video.id}`)
//         }
//     })
// }

// async function getVideoList(videoId) {
//     const api_key = "AIzaSyC1-EQwFTWeuWUBsb_-0i4A5dUjgA23Ufc";
//     const searchUrl = `https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id=${videoId}&key=${api_key}`;;

//     const response = await fetch(searchUrl);
//     const data = await response.json();
//     return data
// }

// getBestVideo('Hsc projectile Motion')



async function sendData() {

  const grade = document.getElementById("classSelect").value
  const subject = document.getElementById("subjectSelect").value
  const chapter = document.getElementById("chapterSelect").value
  const videoType = document.getElementById("videoType")

  const response = await fetch("http://127.0.0.1:5000/get_video", 
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(
        {
          grade: grade,
          subject: subject,
          chapter: chapter,
          videoType: videoType
        }
      )
    }
  )
}

document.querySelector(".find-videos-button").addEventListener('click', sendData)