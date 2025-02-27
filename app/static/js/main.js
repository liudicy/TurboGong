document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const status = document.getElementById('status');
    const error = document.getElementById('error');
    const progress = document.getElementById('progress');
    const timeSpent = document.getElementById('timeSpent');
    
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
        const totalRows = parseInt(response.headers.get('X-Total-Rows') || '0');
        let processedRows = 0;
        
        const reader = response.body.getReader();
        const contentLength = +response.headers.get('Content-Length');
        let receivedLength = 0;
        
        return new ReadableStream({
            start(controller) {
                function push() {
                    reader.read().then(({done, value}) => {
                        if (done) {
                            controller.close();
                            return;
                        }
                        
                        receivedLength += value.length;
                        const percentage = (receivedLength / contentLength * 100).toFixed(2);
                        progress.style.width = percentage + '%';
                        progress.textContent = percentage + '%';
                        
                        controller.enqueue(value);
                        push();
                    });
                }
                push();
            }
        });
    })
    .then(stream => new Response(stream))
    .then(response => response.blob())
    .then(blob => {
        const endTime = performance.now();
        const timeElapsed = endTime - startTime;
        timeSpent.textContent = `生成完成，耗时: ${timeElapsed.toFixed(2)}ms`;
        
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'generated_scripts.txt';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        
        // 保持进度条显示一会儿
        setTimeout(() => {
            status.style.display = 'none';
        }, 2000);
    })
    .catch(err => {
        status.style.display = 'none';
        error.textContent = err.message;
        error.style.display = 'block';
    });
}); 