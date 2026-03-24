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

function createVideoCard(video) {
    const card = document.createElement('div');
    card.className = 'video-card';


    card.innerHTML = `
    <div class="iframe-wrapper">
        <iframe src="${video.url}" width="100%" height="315" frameborder="0" allowfullscreen></iframe>
    </div>
    <h3>${video.title}</h3>
    <p>Channel: ${video.channel}</p>
    <p class="video-score">Match Score: ${Math.round(video.score)}</p>
    `;
    return card;
}



async function sendData() {

  const loading = document.getElementById("loading");
  const noResults = document.getElementById("no-results");
  const enterDetails = document.getElementById("no-details")
  const warning = document.getElementById("warning")


  const grade = document.getElementById("classSelect").value
  const subject = document.getElementById("subjectSelect").value
  const chapter = document.getElementById("chapterSelect").value
  const videoType = document.getElementById("videoType").value

  if (!grade || !subject || !chapter || !videoType) {
    enterDetails.style.display = "block"
    return "Error, No data Selected"
  }

  enterDetails.style.display = "none";
  loading.style.display = "block";
  noResults.style.display = "none";

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

  const videos = await response.json();
  loading.style.display = "none";
  warning.style.display = "block";

  if (!videos || videos.length === 0) {
      noResults.style.display = "block";
      return;
  }

  
  const featuredContainer = document.getElementById('featured-video-container');
  const gridContainer = document.getElementById('video-grid');
  
  // Clear previous results
  featuredContainer.innerHTML = "";
  gridContainer.innerHTML = "";

  if (videos && videos.length > 0) {
      // 1. Display the TOP video separately
      const topVideo = videos[0];
      featuredContainer.appendChild(createVideoCard(topVideo));
      document.getElementById('featured-title').style.display = 'block';

      // 2. Display the rest in the grid
      const otherVideos = videos.slice(1);
      if (otherVideos.length > 0) {
          document.getElementById('others-title').style.display = 'block';
          otherVideos.forEach(video => {
              gridContainer.appendChild(createVideoCard(video));
          });
      }
  }
}

document.querySelector(".find-videos-button").addEventListener('click', sendData)