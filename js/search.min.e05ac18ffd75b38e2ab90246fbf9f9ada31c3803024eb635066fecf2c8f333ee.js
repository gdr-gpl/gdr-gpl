const JSON_INDEX_URL=`${window.BASE_URL}index.json`;console.log("Fetch JSON from :",JSON_INDEX_URL);const QUERY_URL_PARAM="query",MAX_HITS_SHOWN=10,FUSE_OPTIONS={keys:[{name:"title",weight:.8},{name:"description",weight:.5},{name:"content",weight:.3}],ignoreLocation:!0,includeMatches:!0,includeScore:!0,minMatchCharLength:2,threshold:.2};let fuse;const getInputEl=()=>document.querySelector("#s"),initFuse=e=>{fuse=new Fuse(e,FUSE_OPTIONS)},getQuery=()=>getInputEl().value.trim(),setUrlParam=e=>{const t=new URL(location.origin+location.pathname);t.search=`${QUERY_URL_PARAM}=${encodeURIComponent(e)}`,window.history.replaceState({},"",t)},doSearchIfUrlParamExists=()=>{const e=new URLSearchParams(window.location.search);if(e.has(QUERY_URL_PARAM)){const t=decodeURIComponent(e.get(QUERY_URL_PARAM));getInputEl().value=t,handleSearchEvent()}},highlightMatches=(e,t)=>{if(!t||t.length===0)return e;let n=e;const s=[];return t.forEach(e=>{e.indices.forEach(([e,t])=>{s.push([e,t])})}),s.sort((e,t)=>t[0]-e[0]),s.forEach(([e,t])=>{n=n.substring(0,e)+`<mark style="background:#fff3cd;">`+n.substring(e,t+1)+`</mark>`+n.substring(t+1)}),n},createHitHtml=e=>{const t=e.item,n=t.url,a=highlightMatches(t.title,e.matches.filter(e=>e.key==="title")),s=t.description?highlightMatches(t.description,e.matches.filter(e=>e.key==="description")):"",o=t.date?new Date(t.date).toLocaleDateString():"",i=t.categories||[];return`
    <article style="border-bottom:1px solid #eee;">
      <h1><a href="${n}" style="text-decoration:none; color:#222;">${a}</a></h1>
       ${o?`<p style="color: #666;font-size: 10px;letter-spacing: 0.1em;">Posted on ${o}</p>`:""}
      <p style="padding: 1em 0;>${s?`${s}`:""} ${t.readmore?`... <a href="${n}">Continue reading →</a>`:""}</p>
      ${i.length>0?`<p style="color: #666;font-size: 10px;letter-spacing: 0.1em;">
         Posted in 
          ${i.map(e=>`<a href="${e.url}" >${e.name}</a>`).join(", ")}
       </p>`:""}
      </article>
  `},getMainContent=()=>document.querySelector("main .content")||document.querySelector("main"),renderHits=e=>{const t=getMainContent();if(!t)return;const n=getQuery(),s=e.slice(0,MAX_HITS_SHOWN).map(createHitHtml).join(`
`);t.innerHTML=`<p style="
    color: #666;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.1em;
    line-height: 2.6em;
    text-transform: uppercase;
">Search Results for: ${n} </p> ${s}`||"<p>Aucun résultat</p>"},handleSearchEvent=()=>{const e=getQuery();if(!e||e.length<1){document.querySelector("#search_results_container").innerHTML="";return}const t=fuse.search(e);setUrlParam(e),renderHits(t)},fetchJsonIndex=()=>{fetch(JSON_INDEX_URL).then(e=>e.json()).then(e=>{initFuse(e);const t=document.querySelector("#s"),n=document.querySelector("#searchform");n&&n.addEventListener("submit",e=>{e.preventDefault(),handleSearchEvent()}),t.addEventListener("keydown",e=>{e.key==="Escape"&&(t.value="",document.querySelector("#search_results_container").innerHTML="")}),doSearchIfUrlParamExists()}).catch(e=>{console.error(`Failed to fetch JSON index: ${e.message}`)})};document.addEventListener("DOMContentLoaded",fetchJsonIndex)