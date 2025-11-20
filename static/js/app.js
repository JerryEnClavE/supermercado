// JavaScript para SuperMarket

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Manejar precios especiales
    const especialCheckbox = document.getElementById('es_especial');
    const precioEspecialContainer = document.getElementById('precio-especial-container');
    
    if (especialCheckbox && precioEspecialContainer) {
        especialCheckbox.addEventListener('change', function() {
            if (this.checked) {
                precioEspecialContainer.style.display = 'block';
                // Auto-calcular 20% de descuento si no hay precio especial
                const precioNormal = document.getElementById('precio');
                const precioEspecial = document.getElementById('precio_especial');
                
                if (precioNormal && precioEspecial && !precioEspecial.value) {
                    const precio = parseFloat(precioNormal.value);
                    if (precio && !isNaN(precio)) {
                        precioEspecial.value = (precio * 0.8).toFixed(2);
                    }
                }
            } else {
                precioEspecialContainer.style.display = 'none';
            }
        });
    }

    // Validación de formularios
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let valid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    valid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!valid) {
                e.preventDefault();
                showAlert('Por favor, completa todos los campos requeridos.', 'warning');
            }
        });
    });

    // Búsqueda en tiempo real (si existe)
    const searchInput = document.querySelector('input[name="q"]');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (this.value.length >= 2 || this.value.length === 0) {
                    this.form.submit();
                }
            }, 500);
        });
    }

    // Animaciones para cards
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.classList.add('fade-in-up');
    });

    // Manejar eliminación de productos
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('¿Estás seguro de que quieres eliminar este producto? Esta acción no se puede deshacer.')) {
                e.preventDefault();
            }
        });
    });
});

// Función para mostrar alertas personalizadas
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insertar al inicio del contenedor principal
    const container = document.querySelector('.container') || document.querySelector('.container-fluid');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-remover después de 5 segundos
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Función para formatear precios
function formatPrice(price) {
    return new Intl.NumberFormat('es-AR', {
        style: 'currency',
        currency: 'ARS'
    }).format(price);
}

// Función para cargar productos por categoría
function loadProductsByCategory(category) {
    showAlert(`Cargando productos de ${category}...`, 'info');
    // Aquí se podría implementar carga AJAX
}

// Exportar funciones para uso global
window.SuperMarket = {
    showAlert,
    formatPrice,
    loadProductsByCategory
};