function displayQuestion(answer) {

  //document.getElementById(answer + 'Question').style.display = "block";

  if (answer == "no") { // hide the div that is not selected

    document.getElementById('yesQuestion').style.display = "none";

  } else if(answer == 'yes')
  {
    document.getElementById('yesQuestion').style.display = "block";
  }

}
