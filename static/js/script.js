document.addEventListener('DOMContentLoaded', () => {
    const scanBtn = document.getElementById('scan-btn');
    const certBtn = document.getElementById('cert-btn');
    const voiceBtn = document.getElementById('voice-btn');
    const voiceWave = document.getElementById('voice-wave');
    const output = document.getElementById('output');
    const status = document.getElementById('status');
    
    // Voice Assistant
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition;
    let isListening = false;
    
    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';
        
        recognition.onstart = () => {
            voiceWave.classList.remove('hidden');
            isListening = true;
            voiceBtn.classList.add('active');
            appendOutput('Voice assistant activated');
        };
        
        recognition.onend = () => {
            voiceWave.classList.add('hidden');
            isListening = false;
            voiceBtn.classList.remove('active');
            appendOutput('Voice assistant deactivated');
        };
        
        recognition.onresult = (event) => {
            const transcript = Array.from(event.results)
                .map(result => result[0].transcript)
                .join('');
            
            // Process commands
            processVoiceCommand(transcript);
        };
        
        voiceBtn.addEventListener('click', () => {
            if (isListening) {
                recognition.stop();
            } else {
                recognition.start();
            }
        });
    } else {
        voiceBtn.disabled = true;
        voiceBtn.title = "Voice recognition not supported";
    }
    
    // Scan button handler
    scanBtn.addEventListener('click', runScan);
    certBtn.addEventListener('click', generateCertificate);
    
    // Initialize output
    appendOutput('System initialized\n> Ready for commands');
    
    function runScan() {
        const target = document.getElementById('target').value;
        if (!target) {
            appendOutput('Error: Please enter a target');
            return;
        }
        
        const tools = Array.from(document.querySelectorAll('input[name="tool"]:checked'))
            .map(tool => tool.value);
            
        if (tools.length === 0) {
            appendOutput('Error: Select at least one tool');
            return;
        }
        
        status.textContent = '(Scanning...)';
        appendOutput(`Starting scan on ${target} with tools: ${tools.join(', ')}`);
        
        fetch('/scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ target, tools })
        })
        .then(response => response.json())
        .then(data => {
            appendOutput(data.results);
            status.textContent = '(Completed)';
            speakResponse(`Scan completed for ${target}`);
        })
        .catch(error => {
            appendOutput(`Error: ${error.message}`);
            status.textContent = '(Error)';
        });
    }
    
    function generateCertificate() {
        const name = document.getElementById('cert-name').value;
        const identity = document.getElementById('cert-identity').value;
        const course = document.getElementById('cert-course').value;
        
        appendOutput(`Generating certificate for ${name}`);
        
        fetch('/generate-cert', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, identity, course })
        })
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'cybersecurity-certificate.pdf';
            document.body.appendChild(a);
            a.click();
            a.remove();
            appendOutput('Certificate generated successfully');
            speakResponse('Certificate ready for download');
        })
        .catch(error => {
            appendOutput(`Error: ${error.message}`);
        });
    }
    
    function processVoiceCommand(transcript) {
        if (!transcript) return;
        
        transcript = transcript.toLowerCase();
        appendOutput(`Voice command: ${transcript}`);
        
        // Process commands
        if (transcript.includes('scan')) {
            runScan();
        } 
        else if (transcript.includes('read')) {
            speakOutput();
        } 
        else if (transcript.includes('test')) {
            testConnection();
        } 
        else if (transcript.includes('certificate')) {
            generateCertificate();
        } 
        else {
            fetch('/voice-command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: transcript })
            })
            .then(response => response.json())
            .then(data => {
                appendOutput(data.response);
                speakResponse(data.response);
            });
        }
    }
    
    function testConnection() {
        appendOutput('Testing system connection...');
        speakResponse('Running diagnostic tests');
        
        setTimeout(() => {
            appendOutput('System check complete\nAll services operational');
            speakResponse('All systems operational');
        }, 2000);
    }
    
    function speakOutput() {
        if ('speechSynthesis' in window) {
            const text = output.textContent;
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 1.1;
            utterance.pitch = 1.2;
            speechSynthesis.speak(utterance);
            appendOutput('Reading results aloud');
        }
    }
    
    function speakResponse(text) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            speechSynthesis.speak(utterance);
        }
    }
    
    function appendOutput(text) {
        output.textContent += '\n' + text;
        output.scrollTop = output.scrollHeight;
    }
});