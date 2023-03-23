// import axios from 'axios';

click_to_convert.addEventListener('click',function(){

    var speech = true;
    window.SpeechRecognition = window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    // const axios = require("axios");
    recognition.interimResults = true;

    recognition.addEventListener('result', e=>{
        const transcript = Array.from(e.results)
        .map(result => result[0])
        .map(result => result.transcript)

        convert_text.innerHTML = transcript;
        axios.get('localhost:3000', {
            prompt: transcript
        }).then(resp => {
            console.log(resp)
            answer_text.innerHTML = resp
        });
    })

    if(speech == true){
        recognition.start();
    }

})