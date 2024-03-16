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
    ];

    const l = questions.length;
    let selectedOptions = [];
    let op = new Set();
    let count = 0;

    function selectOption(questionIndex, optionIndex) {
        document.querySelectorAll(`.option${questionIndex}`).forEach(option => {
            option.classList.remove('selected');
        });

        const selectedButton = document.querySelector(`#option_${questionIndex}_${optionIndex}`);
        selectedButton.classList.add('selected');

        selectedOptions[questionIndex] = { question: questions[questionIndex].question, option: optionIndex + 1 };

        if (!op.has(questionIndex + 1)) {
            op.add(questionIndex + 1);
            count++;
        }
    }

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

<div class="header">
    <h1>Test de habilidad</h1>
    <p>Marca si es 1, es poco probable que lo hagas, y 5, muy probable.</p>
</div>

<div>
    {#each questions as question, questionIndex}
    <!-- Pregunta -->
    <div class="question-container">
        <h2 class="question-heading">Pregunta {questionIndex + 1}</h2>
        <h3 class="question-text">{question.question}</h3>

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
</div>

{#if count == l}
<button class="button" on:click={finish}>Continuar</button>
{/if}

<style>
    .header {
        background-color: white;
        color: #4659cd;
        padding: 20px;
        text-align: center;
    }

    .header h1 {
        margin: 0;
        font-size: 20px; /* Reducido de 24px */
    }

    .header p {
        margin: 10px 0 0;
        font-size: 14px; /* Reducido de 16px */
    }

    .question-container {
        background-color: #4d59c9;
        padding: 10px;
        margin-bottom: 20px;
        border-radius: 8px;
    }

    .options-container {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }

    .option {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: rgba(0, 0, 0, 0.268);
        color: #ffffff;
        font-size: 14px; /* Reducido de 16px */
        cursor: pointer;
        margin: 2px;
    }

    .option.selected {
        background-color: #ffffff;
        color: rgb(0, 0, 0);
    }

    .button {
        background-color: #4659cd;
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: block;
        margin: 20px auto;
        font-size: 16px;
    }

    .question-heading {
        color: white;
        margin-bottom: 5px;
    }

    .question-text {
        font-size: 16px; /* Reducido de 18px */
        color: white;
    }
</style>
