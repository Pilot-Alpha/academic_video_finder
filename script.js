import {data} from "./data/data.js";

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