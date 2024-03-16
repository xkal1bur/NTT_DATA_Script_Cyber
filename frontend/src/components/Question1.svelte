<!-- Questionnaire.svelte -->
<script>
    import { navigate } from 'svelte-routing';
    let questions = [
        { question: "¿Qué tan satisfecho estás con nuestro servicio?" },
        { question: "¿Cuál es tu nivel de acuerdo con la siguiente afirmación?" }
        // Agrega más objetos para más preguntas si es necesario
    ];

    const l = questions.length;
    // Inicializa una lista para almacenar los pares de pregunta y opción seleccionada
    let selectedOptions = [];

    let op = new Set();
    let count = 0;

    // Función para seleccionar una opción
    function selectOption(questionIndex, optionIndex) {
        selectedOptions[questionIndex] = { question: questions[questionIndex].question, option: optionIndex + 1 };
        console.log(selectedOptions);
        if (!op.has(questionIndex+1)){
            op.add(questionIndex+1);
            count++;
        }
        
        console.log(op.size);
        console.log(questions.length);
    }

    // Función para continuar
    function finish() {
        // Aquí puedes agregar la lógica para guardar las respuestas o pasar a la siguiente pregunta
        //console.log("Respuestas guardadas:", selectedOptions);
        navigate("/register_50")
    }
</script>

{#each questions as question, questionIndex}
    <div>
        <!-- Pregunta -->
        <h1 id="number-question">Pregunta {questionIndex + 1}</h1>
        <h2>{question.question}</h2>

        <!-- Contenedor de opciones -->
        <div class="options-container" id="buttons">
            <!-- Opciones de respuesta -->
            {#each Array.from({ length: 5 }) as _, optionIndex}
                <div class="option" tabindex="0" on:click={() => selectOption(questionIndex, optionIndex)} on:keydown|preventDefault={(e) => e.key === 'Enter' && selectOption(questionIndex, optionIndex)} role="button" aria-label="Seleccionar opción {optionIndex + 1}">{optionIndex + 1}</div>
            {/each}
        </div>
    </div>
{/each}



{#if count==l}
    <button class="button" on:click={finish}>Continuar</button>
{/if}



<style>
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
        background-color: #04AA6D; /* Color de fondo del botón */
        color: white; /* Color del texto del botón */
        font-size: 16px; /* Tamaño del texto del botón */
        cursor: pointer; /* Cambia el cursor al pasar sobre el botón */
        margin: 2px;
    }

    .button {
        background-color: #04AA6D;
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
