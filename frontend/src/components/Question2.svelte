<script>
    // Importa las librerías necesarias
    import { onMount } from 'svelte';
    
    // Define los datos del usuario
    let user = {
        name: 'Antonio',
        age: 50,
        origin: 'Huancayo',
        description: 'Antonio es un líder excepcional, destacándose por su habilidad para organizar equipos, motivar a otros y tomar decisiones estratégicas. Es perseverante ante los desafíos y posee un pensamiento crítico agudo, lo que le permite encontrar soluciones innovadoras y promover el cambio positivo en su entorno.'
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
</script>

<div class="header">
    <h1>Resultados</h1>
    <h2><span style="font-size: 1.5em;">Perfil de tu usuario</span></h2>
</div>

<div class="profile-container">
    <img src="user1.jpg" alt="Foto de perfil" class="profile-image" style="width: 200px; height: 200px;">
    <div class="user-details">
        <h3>{user.name}</h3>
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
