document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const status = document.getElementById('status');
    const error = document.getElementById('error');
    const progress = document.getElementById('progress');
    const timeSpent = document.getElementById('timeSpent');
    const totalSavedTimeSpan = document.getElementById('totalSavedTime');

    function createConfetti() {
        for (let i = 0; i < 50; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + 'vw';
            confetti.style.animationDelay = Math.random() * 2 + 's';
            document.body.appendChild(confetti);
            setTimeout(() => confetti.remove(), 3000);
        }
    }

    function showSuccessMessage(savedTime) {
        const message = document.createElement('div');
        message.className = 'success-message';
        message.innerHTML = `本次脚本生成又为你节省了 ${savedTime.toFixed(1)} 秒，加油打工人🥳`;
        document.body.appendChild(message);
        setTimeout(() => message.remove(), 5000);
    }
    
    // 重置状态
    status.style.display = 'block';
    error.style.display = 'none';
    progress.style.width = '0%';
    progress.textContent = '0%';
    timeSpent.textContent = '';
    
    const startTime = performance.now();
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error);
            });
        }
        
        // 获取总行数
        const totalRows = response.headers.get('X-Total-Rows');
        const savedTime = parseFloat(response.headers.get('X-Saved-Time'));
        const totalSavedTime = parseFloat(response.headers.get('X-Total-Saved-Time'));
        
        // 更新累计节省时间显示
        totalSavedTimeSpan.textContent = totalSavedTime.toFixed(1);
        
        // 显示成功消息和特效
        showSuccessMessage(savedTime);
        createConfetti();
        
        // 计算并显示本次处理时间
        const endTime = performance.now();
        const timeElapsed = ((endTime - startTime) / 1000).toFixed(2);
        timeSpent.textContent = `本次处理用时：${timeElapsed} 秒`;
        
        return response.blob();
    })
    .then(blob => {
        const endTime = performance.now();
        const timeElapsed = endTime - startTime;
        // 隐藏进度条和加载动画
        status.style.display = 'none';
        timeSpent.textContent = `生成完成，耗时: ${(timeElapsed/1000).toFixed(2)}秒`;
        
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'generated_scripts.txt';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
    })
    .catch(err => {
        error.textContent = err.message;
        error.style.display = 'block';
        status.style.display = 'none';
    });
});