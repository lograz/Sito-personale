// script.js

document.addEventListener("DOMContentLoaded", () => {
    // Simulate an API request or any async operation
    setTimeout(() => {
        
        showContent();
    }, 500); // Replace with your actual data loading logic and time

    

    function showContent() {
        const content = document.getElementById("content");
        
        document.getElementById("content").classList.add("contentani")
       
    }
});

const template = document.createElement('template');
template.innerHTML = 
`<style>
.container {
 
  
  max-width: 1440px;
  margin: auto;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  align-content: stretch;
  justify-content: space-around;
  align-items: flex-start;
  padding: 22px;
  gap: 22px;
}
.row {
  width: 100%;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: space-between;
  align-content: stretch;
  align-items: stretch;
  gap: 22px;
}

.col {
  flex-grow: 1;
}

ul {
  display: flex;
  list-style: none;
  gap: 16px;
  padding: 0;
}

li {
  font-size: 14px;
  font-weight: 700;
}

li a {
  color: #071a2b !important;
}

.row.footer {
  align-items: center;
}

.last-update {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  flex-direction: row;
}
</style>
<div  class=" container">
<div class="row footer">
<div class="col-8">
  <span>Designed and Developed by me (Lorenzo Gravina) with Figma, HTML, CSS and JS</span>
</div>
<div class="col-4 last-update">
  <ul>
    <li>
      <a href="https://www.linkedin.com/in/lorenzo-gravina-a4175037/">LINKEDIN</a>
    </li>
    <li>
      <a href="https://dribbble.com/lorenzogravina">DRIBBBLE</a>
    </li>
    <li>
      <a href="https://www.figma.com/@gravinalorenzo">FIGMA</a>
    </li>
  </ul>
</div>
</div>
</div>`

;

class FooterCustom extends HTMLElement {
    constructor(){
        super();
        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));
    }
}

window.customElements.define('footer-custom', FooterCustom)

const cards = document.querySelectorAll(".card_due");
const wrapper = document.querySelector(".cards_uno");

wrapper.addEventListener("mousemove", function ($event) {
	cards.forEach((card) => {
		const rect = card.getBoundingClientRect();
		const x = $event.clientX - rect.left;
		const y = $event.clientY - rect.top;

		card.style.setProperty("--xPos", `${x}px`);
		card.style.setProperty("--yPos", `${y}px`);
	});
});

