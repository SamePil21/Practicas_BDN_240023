const fs = require('fs');
const vm = require('vm');
const assert = require('assert');
const ids = ['tables','objects','q','mod','pre','empty','print','jump','jumpname'];
const nodes = Object.fromEntries(ids.map(id => [id, {id, innerHTML:'', value:'', hidden:false, dataset:{}, addEventListener(){}, insertAdjacentHTML(){}}]));
const filters = ['q','mod','pre','empty'].map(id=>nodes[id]);
const document = {
  body:{dataset:{page:'dict'},insertAdjacentHTML(){}},
  querySelector(selector){if(!selector.startsWith('#')) throw new Error('Selector inesperado '+selector); const id=selector.slice(1); if(!nodes[id]) throw new Error('ID ausente: '+id); return nodes[id]},
  querySelectorAll(selector){return selector==='.filter'?filters:[]}
};
const context={document,Intl,URLSearchParams,location:{search:''},print(){},navigator:{},console,setTimeout,encodeURIComponent}; context.window=context;
vm.createContext(context);
vm.runInContext(fs.readFileSync('datos_bd.js','utf8'),context,{filename:'datos_bd.js'});

vm.runInContext(fs.readFileSync('app.js','utf8'),context,{filename:'app.js'});
const tables=(nodes.tables.innerHTML.match(/class="glass tablecard"/g)||[]).length;
const rows=(nodes.tables.innerHTML.match(/<tbody>/g)||[]).length;
const objects=(nodes.objects.innerHTML.match(/class="section objsection"/g)||[]).length;
const entries=(nodes.objects.innerHTML.match(/<details class="miniitem"><summary>/g)||[]).length;
const expectedRows=Object.values(context.DB_DATA.tables).reduce((n,t)=>n+t.columns.length,0);
assert.equal(tables,25,'debe generar 25 fichas');
assert.equal(rows,25,'cada tabla debe incluir su tabla de atributos');
assert.equal(objects,5,'debe generar cinco categorías de objetos');
assert.equal(entries,108,'debe listar 26 vistas, 6 funciones, 2 procedimientos, 2 eventos y 72 triggers');
assert.equal((nodes.tables.innerHTML.match(/<tbody>/g)||[]).length,25);
assert.equal(context.DB_DATA.totalRows,81292);
for(const name of Object.keys(context.DB_DATA.tables)) assert(nodes.tables.innerHTML.includes(`id="tbl-${name}"`),`falta ficha ${name}`);
console.log(JSON.stringify({tables,tableAttributeSections:rows,columns:expectedRows,objectSections:objects,listedObjects:entries,totalRows:context.DB_DATA.totalRows,result:'OK'},null,2));

