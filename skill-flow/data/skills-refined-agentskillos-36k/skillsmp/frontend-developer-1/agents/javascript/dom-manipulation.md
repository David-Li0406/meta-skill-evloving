---
name: DOM Manipulation
description: Expert en manipulation du DOM - sélection, modification, événements et patterns
workflows:
  - id: dom-creation
    template: wf-creation
    phase: Production
    name: Développement DOM natif
    duration: ongoing
  - id: dom-optimization
    template: wf-evolution
    phase: Réalisation
    name: Optimisation DOM
    duration: 0.5-1 jour
---

# Agent DOM Manipulation

## Responsabilité

Maîtriser les APIs DOM natives pour manipuler efficacement le document HTML.

## Tu NE fais PAS

- ❌ Utiliser les APIs framework (Virtual DOM React, Vue reactivity) → `frameworks/`
- ❌ Appeler des APIs HTTP (fetch, WebSocket) → `api-integration.md`
- ❌ Créer des animations CSS ou avec bibliothèques → `styling/animations.md`
- ❌ Gérer le state global → `state-management/`

## Sélection d'Éléments

### Méthodes de sélection

```javascript
// Par ID (le plus rapide)
const element = document.getElementById('my-id');

// Par sélecteur CSS (un seul élément)
const button = document.querySelector('.btn-primary');
const form = document.querySelector('form[data-validate]');

// Tous les éléments correspondants
const items = document.querySelectorAll('.list-item');
const buttons = document.querySelectorAll('button[type="submit"]');

// Conversion en array pour méthodes array
const itemsArray = [...document.querySelectorAll('.item')];
const filtered = itemsArray.filter((item) => item.dataset.active === 'true');

// Sélection dans un contexte
const container = document.querySelector('.container');
const innerButton = container.querySelector('.btn');
const innerItems = container.querySelectorAll('.item');

// Collections live (se mettent à jour automatiquement)
const forms = document.forms;
const images = document.images;
const links = document.links;
```

### Traversée du DOM

```javascript
const element = document.querySelector('.current');

// Parents
element.parentElement;
element.parentNode;
element.closest('.ancestor'); // Ancêtre le plus proche

// Enfants
element.children; // HTMLCollection (éléments seulement)
element.childNodes; // NodeList (inclut texte, commentaires)
element.firstElementChild;
element.lastElementChild;

// Frères/Sœurs
element.previousElementSibling;
element.nextElementSibling;

// Vérifications
element.matches('.selector'); // Correspond au sélecteur?
element.contains(otherElement); // Contient l'élément?
```

## Création et Modification

### Créer des éléments

```javascript
// Création simple
const div = document.createElement('div');
div.className = 'card';
div.id = 'card-1';
div.textContent = 'Hello World';

// Attributs
div.setAttribute('data-id', '123');
div.dataset.category = 'featured'; // data-category

// Classes
div.classList.add('active', 'highlighted');
div.classList.remove('hidden');
div.classList.toggle('expanded');
div.classList.replace('old-class', 'new-class');
const hasClass = div.classList.contains('active');

// Styles inline (éviter si possible)
div.style.backgroundColor = 'blue';
div.style.cssText = 'color: white; padding: 10px;';

// HTML (attention XSS!)
div.innerHTML = '<span>Contenu</span>';

// Template plus sûr
const template = document.getElementById('card-template');
const clone = template.content.cloneNode(true);
```

### Insertion d'éléments

```javascript
const parent = document.querySelector('.container');
const newElement = document.createElement('div');
const reference = document.querySelector('.reference');

// Méthodes modernes (préférées)
parent.append(newElement); // À la fin (multiple éléments OK)
parent.prepend(newElement); // Au début
reference.before(newElement); // Avant l'élément
reference.after(newElement); // Après l'élément
reference.replaceWith(newElement); // Remplacer

// Méthodes classiques
parent.appendChild(newElement);
parent.insertBefore(newElement, reference);
parent.replaceChild(newElement, oldElement);

// insertAdjacentHTML (performant pour HTML string)
parent.insertAdjacentHTML('beforebegin', '<div>Before</div>');
parent.insertAdjacentHTML('afterbegin', '<div>First child</div>');
parent.insertAdjacentHTML('beforeend', '<div>Last child</div>');
parent.insertAdjacentHTML('afterend', '<div>After</div>');
```

### Suppression

```javascript
// Moderne
element.remove();

// Classique
parent.removeChild(element);

// Vider un conteneur
container.innerHTML = ''; // Simple mais recrée tout
container.replaceChildren(); // Plus propre

// Supprimer en préservant les event listeners
while (container.firstChild) {
  container.removeChild(container.firstChild);
}
```

## Gestion des Événements

### addEventListener

```javascript
const button = document.querySelector('button');

// Syntaxe de base
button.addEventListener('click', (event) => {
  console.log('Clicked!', event.target);
});

// Avec options
button.addEventListener('click', handleClick, {
  once: true, // Se déclenche une seule fois
  passive: true, // N'appellera pas preventDefault (perf scroll)
  capture: true // Phase de capture au lieu de bubbling
});

// Supprimer un listener
function handleClick(event) {
  console.log('Clicked');
}
button.addEventListener('click', handleClick);
button.removeEventListener('click', handleClick); // Même référence requise
```

### Event Delegation

```javascript
// Au lieu d'attacher à chaque élément
// ❌ Mauvais
document.querySelectorAll('.item').forEach((item) => {
  item.addEventListener('click', handleItemClick);
});

// ✅ Bon - Event delegation
document.querySelector('.list').addEventListener('click', (event) => {
  const item = event.target.closest('.item');
  if (item) {
    handleItemClick(item);
  }
});

// Pattern complet
class ListManager {
  constructor(container) {
    this.container = container;
    this.container.addEventListener('click', this.handleClick.bind(this));
  }

  handleClick(event) {
    const target = event.target;

    if (target.matches('.delete-btn')) {
      this.handleDelete(target.closest('.item'));
    } else if (target.matches('.edit-btn')) {
      this.handleEdit(target.closest('.item'));
    } else if (target.matches('.item')) {
      this.handleSelect(target);
    }
  }

  handleDelete(item) { /* ... */ }
  handleEdit(item) { /* ... */ }
  handleSelect(item) { /* ... */ }
}
```

### Types d'événements courants

```javascript
// Mouse events
element.addEventListener('click', handler);
element.addEventListener('dblclick', handler);
element.addEventListener('mouseenter', handler); // Ne bubble pas
element.addEventListener('mouseleave', handler);
element.addEventListener('mouseover', handler); // Bubble
element.addEventListener('mouseout', handler);

// Keyboard events
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeModal();
  if (e.key === 'Enter' && e.ctrlKey) submit();
});

// Form events
form.addEventListener('submit', (e) => {
  e.preventDefault();
  // Traitement
});

input.addEventListener('input', (e) => {
  // À chaque frappe
});

input.addEventListener('change', (e) => {
  // Quand la valeur change et perd le focus
});

// Focus events
input.addEventListener('focus', handler);
input.addEventListener('blur', handler);
input.addEventListener('focusin', handler); // Bubble

// Scroll et resize
window.addEventListener('scroll', handler, { passive: true });
window.addEventListener('resize', handler);

// Custom events
const customEvent = new CustomEvent('userLoggedIn', {
  detail: { userId: '123', name: 'John' },
  bubbles: true
});
element.dispatchEvent(customEvent);
```

### Contrôle de propagation

```javascript
element.addEventListener('click', (event) => {
  // Empêcher l'action par défaut
  event.preventDefault();

  // Empêcher la propagation aux parents
  event.stopPropagation();

  // Empêcher aussi les autres listeners sur cet élément
  event.stopImmediatePropagation();
});

// Vérifier si on peut preventDefault
if (event.cancelable) {
  event.preventDefault();
}
```

## Formulaires

```javascript
const form = document.querySelector('form');

// Accès aux éléments
const input = form.elements.username; // par name
const inputs = form.elements; // FormData-like collection

// FormData API
form.addEventListener('submit', (event) => {
  event.preventDefault();

  const formData = new FormData(form);

  // Accès aux valeurs
  const username = formData.get('username');
  const tags = formData.getAll('tags'); // Pour checkboxes multiples

  // Conversion en objet
  const data = Object.fromEntries(formData);

  // Envoi
  fetch('/api/submit', {
    method: 'POST',
    body: formData // ou JSON.stringify(data)
  });
});

// Validation native
const input = document.querySelector('input');
input.setCustomValidity('Message d\'erreur personnalisé');
input.reportValidity(); // Affiche l'erreur
form.checkValidity(); // Vérifie tous les champs

// Reset
form.reset();
```

## Optimisation Performance

### Minimiser les reflows

```javascript
// ❌ Mauvais - Multiple reflows
items.forEach((item) => {
  container.appendChild(item);
});

// ✅ Bon - Un seul reflow avec DocumentFragment
const fragment = document.createDocumentFragment();
items.forEach((item) => {
  fragment.appendChild(item);
});
container.appendChild(fragment);

// ✅ Ou avec append (moderne)
container.append(...items);
```

### Batch les modifications de style

```javascript
// ❌ Mauvais - Lectures/écritures alternées
elements.forEach((el) => {
  const height = el.offsetHeight; // Lecture (force reflow)
  el.style.height = height + 10 + 'px'; // Écriture
});

// ✅ Bon - Séparer lectures et écritures
const heights = elements.map((el) => el.offsetHeight); // Toutes les lectures
elements.forEach((el, i) => {
  el.style.height = heights[i] + 10 + 'px'; // Toutes les écritures
});
```

### Debounce et Throttle

```javascript
// Debounce - Attendre que l'utilisateur arrête
function debounce(fn, delay) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

const handleSearch = debounce((query) => {
  fetchResults(query);
}, 300);

input.addEventListener('input', (e) => handleSearch(e.target.value));

// Throttle - Limiter la fréquence
function throttle(fn, limit) {
  let inThrottle;
  return (...args) => {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

window.addEventListener('scroll', throttle(updatePosition, 100), { passive: true });
```

### Intersection Observer

```javascript
// Lazy loading, infinite scroll, animations au scroll
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        // Optionnel : arrêter d'observer
        observer.unobserve(entry.target);
      }
    });
  },
  {
    threshold: 0.1, // 10% visible
    rootMargin: '50px' // Marge autour du viewport
  }
);

document.querySelectorAll('.animate-on-scroll').forEach((el) => {
  observer.observe(el);
});
```

## Mots-clés de routage

`DOM`, `querySelector`, `addEventListener`, `event`, `delegation`, `createElement`, `appendChild`, `innerHTML`, `FormData`, `Intersection Observer`, `debounce`, `throttle`

## Livrables

| Livrable | Description |
|----------|-------------|
| Modules DOM | Code de manipulation DOM avec sélection et event delegation |
| Helpers de performance | Fonctions debounce, throttle et optimisation reflows |
| Scripts d'interaction | Event handlers et logique d'interactivité vanilla JS |
