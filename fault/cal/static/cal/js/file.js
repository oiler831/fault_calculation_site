function Change() {
    var key = exampleselect.value;
    var d1 = document.getElementById("d1");
    var d2 = document.getElementById("d2");
    var d3 = document.getElementById("d3");
    if(key==1){
      d1.style.display="block";
      d2.style.display="none";
      d3.style.display="none"; 
    }
    if(key==2){
      d1.style.display="none";
      d2.style.display="block";
      d3.style.display="none";
    }
    if(key==3){
      d1.style.display="none";
      d2.style.display="none";
      d3.style.display="block";
    }
}

function Hide(){
    var d1 = document.getElementById("d1");
    var d2 = document.getElementById("d2");
    var d3 = document.getElementById("d3");
    d1.style.display="none";
    d2.style.display="none";
    d3.style.display="none";
}

function Reveal(){
  var key = exampleselect.value;
  var d1 = document.getElementById("d1");
  var d2 = document.getElementById("d2");
  var d3 = document.getElementById("d3");
  if(key==1){
    d1.style.display="block";
  }
  if(key==2){
    d2.style.display="block";
  }
  if(key==3){
    d3.style.display="block";
  }
}

function selectActive()  {
  const target1 = document.getElementById('exampleselect');
  target1.disabled = false;
}
  
  function selectDisable()  {
  const target1 = document.getElementById('exampleselect');
  target1.disabled = true;
}

function fileActive()  {
  const target2 = document.getElementById('formFile');
  target2.disabled = false;
}

function fileDisable()  {
  const target2 = document.getElementById('formFile');
  target2.disabled = true;
}