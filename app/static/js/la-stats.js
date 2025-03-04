// 监听51LA统计SDK加载完成
const observer = new MutationObserver((mutations, obs) => {
    if (typeof LA !== 'undefined') {
        // 获取访问量元素
        const visitCountElement = document.getElementById('LA_visit_count');
        
        // 使用51LA的API获取访问量数据
        LA.config.get('pageview').then(function(response) {
            if (response?.data?.pv_count) {
                // 格式化数字显示
                visitCountElement.textContent = Number(response.data.pv_count).toLocaleString('zh-CN');
                obs.disconnect();
            }
        }).catch(function(error) {
            console.error('获取访问量数据失败:', error);
            setTimeout(() => observer.observe(document, config), 3000);
        });
    }
});

// 开始观察DOM变化
const config = { childList: true, subtree: true };
observer.observe(document, config);

// 添加重试机制
window.addEventListener('LA_Ready', function() {
    observer.observe(document, config);
});