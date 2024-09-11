console.log('Hello')

const passInput=document.getElementById('password');
const repassInput=document.getElementById('re-password');
const submitButton=document.getElementById('submit');
const popup = document.getElementById('popup');

function confirmPass(event){
  const pass=passInput.value;
  const repass=repassInput.value;
  if (pass!==repass){
      submitButton.disabled=true;
      event.preventDefault();
      // alert('Passwords do not match!');
      return false;
  }
  else{
      submitButton.disabled=false;
      return true;
  }
}

passInput.addEventListener('keyup',confirmPass)
repassInput.addEventListener('keyup',confirmPass);

repassInput.addEventListener('keyup', () => {
  if (passInput.value === repassInput.value) {
    popup.style.display = 'none'; // Hide the pop-up if passwords match
  } else {
    popup.style.display = 'block'; // Show the pop-up if passwords do not match
  }
});

function updatePlaceholder() {
  const quantityInput = document.getElementsByName('quantity');
  const myElement = quantityInput[0]
  const totalInput = document.getElementsByName('total');
  const price=document.getElementsByName('rate');
  const quantity = myElement.value;
  const rate=price[0].placeholder
  console.log(price[0].placeholder)
  
  const cost=quantity*rate;
  totalInput[0].placeholder = `₹ ${cost}`;
}

window.addEventListener('scroll', function() {
    var buttonContainer = document.getElementById('button-container');
    var scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0;
  
    if (scrollTop > 100) {
      buttonContainer.classList.add('bottom-right');
    } else {
      buttonContainer.classList.remove('bottom-right');
    }
  });
  

