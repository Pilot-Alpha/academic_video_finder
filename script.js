const data = {
  "9": {
    "Bangla 1": ["Chapter 1", "Chapter 2"], // Add your real chapters here
    "Bangla 2": [], "English 1": [], "English 2": [], "Math": [], 
    "Higher Math": [], "Physics": [], "Chemistry": [], "Biology": [], 
    "ICT": [], "BGS": [], "IME": []
  },
  "10": {
    "Bangla 1": [], "Bangla 2": [], "English 1": [], "English 2": [], "Math": [], 
    "Higher Math": [], "Physics": [], "Chemistry": [], "Biology": [], 
    "ICT": [], "BGS": [], "IME": []
  },
  "11": {
    "Bangla 1": [], "Bangla 2": [], "English 1": [], "English 2": [], 
    "Higher Math 1": [], "Higher Math 2": [], "Physics 1": [], "Physics 2": [], 
    "Chemistry 1": [], "Chemistry 2": [], "Biology 1": [], "Biology 2": [], "ICT": []
  },
  "12": {
    "Bangla 1": [], "Bangla 2": [], "English 1": [], "English 2": [], 
    "Higher Math 1": [], "Higher Math 2": [], "Physics 1": [], "Physics 2": [], 
    "Chemistry 1": [], "Chemistry 2": [], "Biology 1": [], "Biology 2": [], "ICT": []
  }
};

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