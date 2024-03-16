<!-- Questionnaire.svelte -->
<script>
    import { navigate } from 'svelte-routing';

    let questions = [
        { question: "Llevar a cabo mis planes." },
        { question: "Perder mi tiempo."},
        { question: "Encontrar difícil ponerme a trabajar."},
        { question: "Desordenar las cosas."},
        { question: "Terminar lo que empiezo."},
        { question: "No concentrar mi mente en la tarea en cuestión."},
        { question: "Hacer las cosas rápidamente."},
        { question: "Siempre saber lo que estoy haciendo."},
        { question: "Posponer decisiones."},
        { question: "Distraerme fácilmente."}
        // Agrega más objetos para más preguntas si es necesario
    ];

    

    const l = questions.length;

    // Inicializa una lista para almacenar los pares de pregunta y opción seleccionada
    let selectedOptions = [];
    let op = new Set();
    let count = 0;

    // Función para seleccionar una opción
    function selectOption(questionIndex, optionIndex) {
        // Limpiar la marca de la última opción seleccionada por pregunta
        document.querySelectorAll(`.option${questionIndex}`).forEach(option => {
            option.classList.remove('selected');
        });

        // Marcar la opción seleccionada en gris
        const selectedButton = document.querySelector(`#option_${questionIndex}_${optionIndex}`);
        selectedButton.classList.add('selected');

        // Actualizar la opción seleccionada en la lista
        selectedOptions[questionIndex] = { question: questions[questionIndex].question, option: optionIndex + 1 };
        console.log(selectedOptions);

        // Incrementar el contador si es la primera vez que se selecciona una opción para esta pregunta
        if (!op.has(questionIndex + 1)) {
            op.add(questionIndex + 1);
            count++;
        }
    }

    // Función para continuar
    function finish() {
        // Aquí puedes agregar la lógica para guardar las respuestas o pasar a la siguiente pregunta
        // console.log("Respuestas guardadas:", selectedOptions);
        let data_enviar = {};
        data_enviar["industriousness"] = selectedOptions;
        data_enviar["first_name"] = "Oscar"
        data_enviar["last_name"] = "Gonzalez"
        data_enviar["job_title"] = "Pintor"

        let json_data = JSON.stringify(data_enviar);

        console.log(json_data)
        fetch('http://localhost:5000/worker', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: json_data
        }).then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Error en la petición');
        }).then(data => {
            console.log(data);
        }).catch(error => {
            console.error('Error:', error);
        });
        navigate("/register_50");
    }
</script>

{#each questions as question, questionIndex}
    <div>
        <!-- Pregunta -->
        <!--<h1 id="number-question">Pregunta {questionIndex + 1}</h1>-->
        <h2>{questionIndex+1}.{question.question}</h2>

        <!-- Contenedor de opciones -->
        <div class="options-container" id="buttons">
            <!-- Opciones de respuesta -->
            {#each Array.from({ length: 5 }) as _, optionIndex}
                <div class="option option{questionIndex}" tabindex="0" on:click={() => selectOption(questionIndex, optionIndex)} on:keydown|preventDefault={(e) => e.key === 'Enter' && selectOption(questionIndex, optionIndex)} role="button" aria-label="Seleccionar opción {optionIndex + 1}" id="option_{questionIndex}_{optionIndex}">{optionIndex + 1}</div>
            {/each}
        </div>
    </div>

    {#if questionIndex !== questions.length - 1}
    <hr class="question-separator" />
    {/if}
{/each}

{#if count == l}
    <button class="button" on:click={finish}>Continuar</button>
{/if}

<style>

    .question-container {
        margin-bottom: 20px; /* Margen inferior para separar las preguntas */
    }


    /* Estilos para las opciones */
    .options-container {
        display: flex;
        justify-content: center; /* Centra horizontalmente los botones */
        margin-top: 20px; /* Espacio superior para separar la pregunta de las opciones */
    }

    .option {
        width: 40px; /* Ancho del botón circular */
        height: 40px; /* Altura del botón circular */
        border-radius: 50%; /* Hace que el botón sea circular */
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #4d59c9; /* Color de fondo del botón */
        color: white; /* Color del texto del botón */
        font-size: 16px; /* Tamaño del texto del botón */
        cursor: pointer; /* Cambia el cursor al pasar sobre el botón */
        margin: 2px;
    }

    .option.selected {
        background-color: gray; /* Color de fondo cuando se presiona */
    }

    .button {
        background-color: #4659cd;
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: block; /* Cambiado a block para centrar horizontalmente */
        margin: 20px auto; /* Centra el botón horizontalmente */
        font-size: 16px;
    }
</style>
