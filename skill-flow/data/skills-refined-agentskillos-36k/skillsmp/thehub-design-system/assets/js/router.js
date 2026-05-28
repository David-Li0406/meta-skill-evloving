const HubRouter=(function(){'use strict';
const content=document.getElementById('page-content');
const main=document.getElementById('main-content');
let navigating=false;

async function fetchContent(url){
  const r=await fetch(url,{headers:{'X-Requested-With':'XMLHttpRequest'}});
  if(!r.ok)throw new Error('HTTP '+r.status);
  return{html:await r.text(),title:r.headers.get('X-Page-Title')||'TheHUB'};
}

async function navigate(url,push=true){
  if(navigating||!url.startsWith('/v3'))return false;
  navigating=true;
  try{
    content.classList.add('loading');
    const{html,title}=await fetchContent(url);
    content.innerHTML=html;
    if(push)history.pushState({url},title,url);
    document.title=title;
    updateNav(url);
    main.scrollTop=0;window.scrollTo(0,0);
    main.focus();
    document.dispatchEvent(new CustomEvent('hub:contentloaded',{detail:{url}}));
  }catch(e){console.error(e);window.location.href=url}
  finally{content.classList.remove('loading');navigating=false}
  return true;
}

function updateNav(url){
  document.querySelectorAll('.sidebar-link,.mobile-nav-link').forEach(l=>l.removeAttribute('aria-current'));
  const path=url.replace('/v3','').replace(/^\//,'')||'dashboard';
  const base=path.split('/')[0]||'dashboard';
  document.querySelectorAll('[data-nav="'+base+'"]').forEach(l=>l.setAttribute('aria-current','page'));
}

function handleClick(e){
  const link=e.target.closest('a[href]');if(!link)return;
  const href=link.getAttribute('href');
  if(!href||href.startsWith('http')||href.startsWith('mailto:')||link.hasAttribute('target')||e.ctrlKey||e.metaKey)return;
  if(href.startsWith('/v3')){e.preventDefault();navigate(href)}
}

function init(){
  history.replaceState({url:window.location.pathname},document.title);
  document.addEventListener('click',handleClick);
  window.addEventListener('popstate',e=>{if(e.state?.url)navigate(e.state.url,false)});
}

return{init,navigate}})();
document.readyState==='loading'?document.addEventListener('DOMContentLoaded',HubRouter.init):HubRouter.init();
