// JavaScript для ограничения доступа редакторов к роли администратора

document.addEventListener('DOMContentLoaded', function() {
    // Проверяем, является ли пользователь редактором
    if (document.body.classList.contains('editor-user')) {
        // Находим все выпадающие списки ролей
        var roleSelects = document.querySelectorAll('select[name*="role"]');
        
        roleSelects.forEach(function(select) {
            // Находим опцию "Администратор" и скрываем её
            for (var i = 0; i < select.options.length; i++) {
                if (select.options[i].value === 'ADMIN' || select.options[i].text === 'Администратор') {
                    // Удаляем опцию полностью, чтобы редактор не мог её выбрать даже через инспектор кода
                    select.remove(i);
                    i--; // Корректируем индекс после удаления
                }
            }
        });
        
        // Дополнительно мониторим изменения в DOM, если элементы добавляются динамически
        var observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.addedNodes.length) {
                    // Проверяем новые селекты
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === 1) { // Элемент
                            // Проверяем внутри нового элемента
                            var newSelects = node.querySelectorAll('select[name*="role"]');
                            if (newSelects.length > 0) {
                                newSelects.forEach(function(select) {
                                    for (var i = 0; i < select.options.length; i++) {
                                        if (select.options[i].value === 'ADMIN' || select.options[i].text === 'Администратор') {
                                            select.remove(i);
                                            i--;
                                        }
                                    }
                                });
                            }
                            
                            // Проверяем, не является ли сам элемент селектом
                            if (node.tagName === 'SELECT' && node.name && node.name.indexOf('role') >= 0) {
                                for (var i = 0; i < node.options.length; i++) {
                                    if (node.options[i].value === 'ADMIN' || node.options[i].text === 'Администратор') {
                                        node.remove(i);
                                        i--;
                                    }
                                }
                            }
                        }
                    });
                }
            });
        });
        
        // Запускаем наблюдатель
        observer.observe(document.body, { childList: true, subtree: true });
    }
}); 