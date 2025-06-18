let emergencyTimeout = setTimeout(() => {
    confirmEmergency();
}, 30000); // 30 segundos

function confirmEmergency() {
    clearTimeout(emergencyTimeout); // Cancela o timeout se o usuário clicar
    // Obtém o token NFC da URL
    const token = window.location.pathname.split('/').pop();
    
    fetch(`/emergency/confirm/${token}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/emergency/success/active';
        } else {
            alert('Erro ao confirmar emergência: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao processar a requisição');
    });
}

function abortEmergency() {
    clearTimeout(emergencyTimeout); // Cancela o timeout se o usuário clicar
    // Obtém o token NFC da URL
    const token = window.location.pathname.split('/').pop();
    
    fetch(`/emergency/abort/${token}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/emergency/success/aborted';
        } else {
            alert('Erro ao abortar emergência: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao processar a requisição');
    });
} 