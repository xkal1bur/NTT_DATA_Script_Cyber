<script>
    // Importa las librerías necesarias
    import { onMount } from 'svelte';
    
    // Define los datos del usuario
    let user = {
        name: 'Antonio',
        last_name: 'Gonzalez',
        age: 50,
        origin: 'Huancayo',
        description: "¡Conoce a Antonio Gonzalez, un carpintero excepcional con un nivel de industriousness del 99.99%! Con 50 años de experiencia en la industria, Antonio se destaca por su dedicación incansable a su oficio. Su habilidad para trabajar de manera eficiente y a un alto nivel de calidad lo convierten en un verdadero experto en su campo. Cuando contratas a Antonio, puedes estar seguro de que recibirás un trabajo impecable y realizado con gran atención a los detalles. No busques más, ¡Antonio es la opción perfecta para tus proyectos de carpintería!"
    };

    // Datos de habilidades del usuario
    let skills = [
        { name: 'Creatividad', percentage: 90 },
        { name: 'Perseverancia', percentage: 85 },
        { name: 'Habilidades de liderazgo', percentage: 80 },
        { name: 'Planificación y organización', percentage: 95 },
        { name: 'Pensamiento crítico.', percentage: 85 },
        { name: 'Gestión del tiempo.', percentage: 80 }
    ];

    // Función para calcular el ancho de la barra de habilidades
    function calculateWidth(percentage) {
        return `${percentage}%`;
    }

    // Ejemplo de uso de onMount para mostrar un mensaje cuando se carga el componente
    onMount(() => {
        console.log('El componente se ha cargado correctamente.');
    });
    
    function recibir_data(){
        fetch('http://localhost:5000/worker/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
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
    }
</script>

<div class="header">
    <h1>Resultados</h1>
    <h2><span style="font-size: 1.5em;">Perfil de tu usuario</span></h2>
</div>

<div class="profile-container">
    <img src="user1.jpg" alt="Foto de perfil" class="profile-image" style="width: 200px; height: 200px;">
    <div class="user-details">
        <h3>{user.name} {user.last_name}</h3>
        <p>Edad: {user.age}</p>
        <p>Procedencia: {user.origin}</p>
        <p>{user.description}</p>
    </div>
</div>

<div class="skills-container">
    <h2><span style="font-size: 1.2em;">Habilidades</span></h2>
    {#each skills as skill}
        <div class="skill-item">
            <p>{skill.name}</p>
            <div class="skill-bar" style="width: {calculateWidth(skill.percentage)};"></div>
        </div>
    {/each}
</div>

<style>
    /* Estilos para la barra de habilidades */
    .skill-bar {
        height: 20px;
        background-color: #4d59c9;
    }

    /* Estilos adicionales para la página */
    .header {
        background-color: #4d59c9;
        color: white;
        padding: 20px;
        text-align: center;
    }

    .profile-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 100px;
    }

    .profile-image {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        margin-right: 20px;
    }

    .user-details {
        text-align: left;
    }

    .skills-container {
        margin: 20px;
    }

    .skill-item {
        margin-bottom: 10px;
    }

    h1, h2, h3, p {
        margin: 0;
    }
</style>
