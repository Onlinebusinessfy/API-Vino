async function predictWineQuality() {
    // Recoger los datos de los inputs
    const fixed_acidity = parseFloat(document.getElementById('fixed_acidity').value);
    const volatile_acidity = parseFloat(document.getElementById('volatile_acidity').value);
    const citric_acid = parseFloat(document.getElementById('citric_acid').value);
    const residual_sugar = parseFloat(document.getElementById('residual_sugar').value);
    const chlorides = parseFloat(document.getElementById('chlorides').value);
    const free_sulfur_dioxide = parseFloat(document.getElementById('free_sulfur_dioxide').value);
    const total_sulfur_dioxide = parseFloat(document.getElementById('total_sulfur_dioxide').value);
    const density = parseFloat(document.getElementById('density').value);
    const pH = parseFloat(document.getElementById('pH').value);
    const sulphates = parseFloat(document.getElementById('sulphates').value);
    const alcohol = parseFloat(document.getElementById('alcohol').value);

    // Verifica que todos los campos sean números válidos
    if (
        isNaN(fixed_acidity) || fixed_acidity < 0 ||
        isNaN(volatile_acidity) || volatile_acidity < 0 ||
        isNaN(citric_acid) || citric_acid < 0 ||
        isNaN(residual_sugar) || residual_sugar < 0 ||
        isNaN(chlorides) || chlorides < 0 ||
        isNaN(free_sulfur_dioxide) || free_sulfur_dioxide < 0 ||
        isNaN(total_sulfur_dioxide) || total_sulfur_dioxide < 0 ||
        isNaN(density) || density < 0 ||
        isNaN(pH) || pH < 0 ||
        isNaN(sulphates) || sulphates < 0 ||
        isNaN(alcohol) || alcohol < 0
    ) {
        document.getElementById('result').innerText = 'Por favor, ingresa valores válidos y no negativos en todos los campos.';
        return;  // Detener la función si hay campos inválidos
    }

    // Crear el objeto con los datos del vino
    const wineData = {
        fixed_acidity,
        volatile_acidity,
        citric_acid,
        residual_sugar,
        chlorides,
        free_sulfur_dioxide,
        total_sulfur_dioxide,
        density,
        pH,
        sulphates,
        alcohol
    };

    // Agrega un log para verificar los datos antes de la solicitud
    console.log('Datos enviados:', wineData);  // Log de los datos del vino

    // Hacer la petición al servidor
    try {
        const response = await fetch('http://127.0.0.1:8000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(wineData)  // Asegúrate de que aquí estás enviando el objeto
        });

        // Procesar la respuesta
        if (response.ok) {
            const result = await response.json();
            document.getElementById('result').innerText = `Calidad Predicha: ${result.quality}`;
        } else {
            // Leer el error desde el servidor
            const error = await response.json();
            console.error('Error en la respuesta del servidor:', error);  // Log del error
            // Mostrar el error en un formato más legible
            document.getElementById('result').innerText = `Error: ${error.detail || 'Ocurrió un error inesperado.'}`;
        }
    } catch (error) {
        console.error('Error de red:', error);  // Log de errores de red
        document.getElementById('result').innerText = `Error de red: ${error.message}`;
    }
}
