function toggle_display(){
  el = document.querySelector('.report');

  if(el.style.visibility == 'hidden'){
      el.style.visibility = 'visible'
  }else{
     el.style.visibility = 'hidden'
  }
}