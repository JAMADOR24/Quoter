// Primero, manejar habilitar/deshabilitar cantidad cuando cambie un checkbox
document.querySelectorAll('input[type=checkbox]').forEach(cb => {
    cb.addEventListener('change', (e) => {
        const id = e.target.value;
        const cantidadInput = document.getElementById('cantidad_' + id);
        cantidadInput.disabled = !e.target.checked;
    });
});

// Luego, manejar el submit del formulario
document.getElementById("cotizacionForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const cliente = document.getElementById("cliente").value;
    const seleccionados = document.querySelectorAll("input[name='item']:checked");
    const items = [];

    seleccionados.forEach(input => {
        const id = parseInt(input.value);
        const cantidad = parseInt(document.getElementById('cantidad_' + id).value);
        items.push({ item_id: id, cantidad });
    });

    const response = await fetch("/crear-cotizacion", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cliente, items })
    });

    const result = await response.json();

    if (result.success) {
        document.getElementById("resultado").innerHTML = `
            <p>PDF generado con éxito: 
                <a href="/descargar/${result.archivo}" target="_blank">${result.archivo}</a>
            </p>`;
    } else {
        document.getElementById("resultado").innerText = "Hubo un error generando la cotización.";
    }
});
