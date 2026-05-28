const HubApp=(function(){'use strict';
function handleTableClick(e){
  const row=e.target.closest('tr[data-href]');
  if(row&&!e.target.closest('a,button'))HubRouter.navigate(row.dataset.href);
}
function initInteractive(){
  document.querySelectorAll('.table--clickable').forEach(t=>t.addEventListener('click',handleTableClick));
}
function init(){initInteractive();document.addEventListener('hub:contentloaded',initInteractive)}
return{init}})();
document.readyState==='loading'?document.addEventListener('DOMContentLoaded',HubApp.init):HubApp.init();
