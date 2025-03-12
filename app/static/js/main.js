document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('uploadForm');
    const status = document.getElementById('status');
    const error = document.getElementById('error');
    const progress = document.getElementById('progress');
    const timeSpent = document.getElementById('timeSpent');
    const totalSavedTimeSpan = document.getElementById('totalSavedTime');

    // 创建彩色纸屑效果
    function createConfetti() {
        const confettiCount = 80; // 增加纸屑数量
        const colors = ['#0071e3', '#34c759', '#ff9500', '#5e5ce6', '#ff3b30'];
        
        for (let i = 0; i < confettiCount; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + 'vw';
            confetti.style.animationDelay = Math.random() * 3 + 's';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            document.body.appendChild(confetti);
            
            // 自动清理DOM
            setTimeout(() => {
                if (confetti && confetti.parentNode) {
                    confetti.parentNode.removeChild(confetti);
                }
            }, 5000);
        }
    }

    // 显示成功消息
    function showSuccessMessage(savedTime) {
        const message = document.createElement('div');
        message.className = 'success-message';
        message.innerHTML = `<div style="font-size: 24px; margin-bottom: 10px;">🎉</div>本次脚本生成为你节省了 <strong>${savedTime.toFixed(1)}</strong> 秒<div style="margin-top: 8px; font-size: 14px;">加油打工人！</div>`;
        document.body.appendChild(message);
        
        // 自动清理DOM
        setTimeout(() => {
            if (message && message.parentNode) {
                message.style.opacity = '0';
                message.style.transform = 'translate(-50%, -40%)';
                message.style.transition = 'all 0.5s ease';
                
                setTimeout(() => {
                    if (message && message.parentNode) {
                        message.parentNode.removeChild(message);
                    }
                }, 500);
            }
        }, 4000);
    }
    
    // 表单提交处理
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            // 验证文件
            const templateFile = formData.get('template');
            const dataFile = formData.get('data');
            
            if (!templateFile || !templateFile.name) {
                showError('请选择模板文件');
                return;
            }
            
            if (!dataFile || !dataFile.name) {
                showError('请选择数据文件');
                return;
            }
            
            // 验证文件类型
            if (!templateFile.name.toLowerCase().endsWith('.txt')) {
                showError('模板文件必须是.txt格式');
                return;
            }
            
            if (!dataFile.name.toLowerCase().endsWith('.xlsx') && !dataFile.name.toLowerCase().endsWith('.xls')) {
                showError('数据文件必须是.xlsx或.xls格式');
                return;
            }
            
            // 重置状态
            resetUI();
            
            // 显示加载状态
            status.style.display = 'block';
            
            const startTime = performance.now();
            
            // 发送请求
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.error || '生成脚本时发生错误');
                    });
                }
                
                // 获取响应头信息
                const savedTime = parseFloat(response.headers.get('X-Saved-Time') || '0');
                const totalSavedTime = parseFloat(response.headers.get('X-Total-Saved-Time') || '0');
                
                // 更新累计节省时间显示
                if (totalSavedTimeSpan) {
                    totalSavedTimeSpan.textContent = totalSavedTime.toFixed(1);
                    // 添加数字变化动画
                    totalSavedTimeSpan.classList.add('highlight');
                    setTimeout(() => {
                        totalSavedTimeSpan.classList.remove('highlight');
                    }, 2000);
                }
                
                // 显示成功消息和特效
                showSuccessMessage(savedTime);
                createConfetti();
                
                // 计算并显示本次处理时间
                const endTime = performance.now();
                const timeElapsed = ((endTime - startTime) / 1000).toFixed(2);
                if (timeSpent) {
                    timeSpent.textContent = `本次处理用时：${timeElapsed} 秒`;
                }
                
                return response.blob();
            })
            .then(blob => {
                // 隐藏进度条和加载动画
                if (status) {
                    status.style.display = 'none';
                }
                
                // 下载生成的文件
                downloadFile(blob);
            })
            .catch(err => {
                showError(err.message || '处理请求时发生错误');
            });
        });
    }
    
    // 辅助函数
    function resetUI() {
        if (status) status.style.display = 'none';
        if (error) {
            error.style.display = 'none';
            error.textContent = '';
        }
        if (progress) {
            progress.style.width = '0%';
            progress.textContent = '';
        }
        if (timeSpent) timeSpent.textContent = '';
    }
    
    function showError(message) {
        if (error) {
            error.textContent = message;
            error.style.display = 'block';
        }
        if (status) status.style.display = 'none';
    }
    
    function downloadFile(blob) {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'generated_scripts.txt';
        document.body.appendChild(a);
        a.click();
        
        // 清理
        setTimeout(() => {
            window.URL.revokeObjectURL(url);
            if (a && a.parentNode) {
                a.parentNode.removeChild(a);
            }
        }, 100);
    }
    
    // 文件输入框美化
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const fileName = this.files[0]?.name;
            if (fileName) {
                this.title = fileName;
                this.classList.add('has-file');
            } else {
                this.title = '';
                this.classList.remove('has-file');
            }
        });
    });
});