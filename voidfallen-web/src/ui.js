export function printToTerminal(text, className = 'narrative') {
    const output = document.getElementById('output');
    const para = document.createElement('p');
    para.textContent = text;
    para.className = className;
    output.appendChild(para);
    output.scrollTop = output.scrollHeight;
}