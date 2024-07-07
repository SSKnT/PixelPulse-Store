particlesJS('particles-js', {
    particles: {
      number: {
        value: 50,
        density: {
          enable: true,
          value_area: 100
        }
      },
      color: {
        value: '#ffffff' // Red color
      },
      shape: {
        type: 'circle'
      },
      size: {
        value:1
      },
      line_linked: {
        enable: true,
    color:'#ffffff'
      }
    },
    interactivity: {
      detect_on: 'canvas',
      events: {
        onhover: {
          enable: false,
          mode: 'repulse',
          distance: 1,
        }
      }
    },
    retina_detect: true
  });
