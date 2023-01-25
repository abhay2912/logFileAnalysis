let otp = $('.otp').hide();
let clock = document.querySelector('.ContentWrapper');
let home = document.querySelector('.home');
// Starting of Clock

function UpdateClock() {
	var time = new Date();
	var Hour = time.getHours() % 12 ? time.getHours() % 12 : 12;
	var Minute = time.getMinutes() < 10 ? "0" + time.getMinutes() : time.getMinutes();
	var Meridiem = time.getHours() < 12 ? "AM" : "PM";
	var Clock = document.getElementsByClassName("Clock")[0];
	Clock.getElementsByClassName("Hour")[0].children[0].innerHTML = Hour;
	Clock.getElementsByClassName("Colon")[0].classList.toggle("blink");
	Clock.getElementsByClassName("Minute")[0].children[0].innerHTML = Minute;
	Clock.getElementsByClassName("Meridiem")[0].children[0].innerHTML = Meridiem;
	setTimeout(UpdateClock, 1000);
}

UpdateClock();

// Ending of Clock

//Starting of pressing Enter.

document.body.addEventListener('keypress',(e) =>{
    if (e.key == 'Enter')
    {
        
        home.classList.add('blur'); // Adding blured effect.
        clock.classList.add('cblur');
        otp.show(500);


    }
})

//Ending of Pressing Enter.

//Starting of OTP

const inputs = document.querySelectorAll(".otp-field input");

inputs.forEach((input, index) => {
    input.dataset.index = index;
    input.addEventListener("keyup", handleOtp);
    input.addEventListener("paste", handleOnPasteOtp);
});

function handleOtp(e) {
    /**
     * <input type="text" 👉 maxlength="1" />
     * 👉 NOTE: On mobile devices `maxlength` property isn't supported,
     * So we to write our own logic to make it work. 🙂
     */
    const input = e.target;
    let value = input.value;
    let isValidInput = value.match(/[0-9a-z]/gi);
    input.value = "";
    input.value = isValidInput ? value[0] : "";

    let fieldIndex = input.dataset.index;
    if (fieldIndex < inputs.length - 1 && isValidInput) {
        input.nextElementSibling.focus();
    }

    if (e.key === "Backspace" && fieldIndex > 0) {
        input.previousElementSibling.focus();
    }

    if (fieldIndex == inputs.length - 1 && isValidInput) {
        submit();
    }
}

function handleOnPasteOtp(e) {
    const data = e.clipboardData.getData("text");
    const value = data.split("");
    if (value.length === inputs.length) {
        inputs.forEach((input, index) => (input.value = value[index]));
        submit();
    }
}

function submit() {
    console.log("Submitting...");
    // 👇 Entered OTP
    let inpotp = "";
    inputs.forEach((input) => {
        inpotp += input.value;
        input.disabled = true;
        input.classList.add("disabled");
    });
    if(inpotp == '123456')
        {
            window.location.replace("http://127.0.0.1:5000/upload");
            $('.otp').hide();
            clock.classList.remove('cblur');
            home.classList.remove('blur');
        }
    console.log(inpotp);
    // 👉 Call API below
}


//Ending of OTP