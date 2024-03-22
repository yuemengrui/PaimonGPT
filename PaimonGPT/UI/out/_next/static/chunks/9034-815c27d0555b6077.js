"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[9034],{5523:function(e,t,n){async function r(e,t){let n;let r=e.getReader();for(;!(n=await r.read()).done;)t(n.value)}function a(){return{data:"",event:"",id:"",retry:void 0}}n.d(t,{L:function(){return u}});var s=function(e,t){var n={};for(var r in e)Object.prototype.hasOwnProperty.call(e,r)&&0>t.indexOf(r)&&(n[r]=e[r]);if(null!=e&&"function"==typeof Object.getOwnPropertySymbols)for(var a=0,r=Object.getOwnPropertySymbols(e);a<r.length;a++)0>t.indexOf(r[a])&&Object.prototype.propertyIsEnumerable.call(e,r[a])&&(n[r[a]]=e[r[a]]);return n};let i="text/event-stream",l="last-event-id";function u(e,t){var{signal:n,headers:u,onopen:d,onmessage:c,onclose:f,onerror:b,openWhenHidden:h,fetch:v}=t,m=s(t,["signal","headers","onopen","onmessage","onclose","onerror","openWhenHidden","fetch"]);return new Promise((t,s)=>{let p;let y=Object.assign({},u);function x(){p.abort(),document.hidden||k()}y.accept||(y.accept=i),h||document.addEventListener("visibilitychange",x);let g=1e3,N=0;function E(){document.removeEventListener("visibilitychange",x),window.clearTimeout(N),p.abort()}null==n||n.addEventListener("abort",()=>{E(),t()});let w=null!=v?v:window.fetch,T=null!=d?d:o;async function k(){var n,i;p=new AbortController;try{let n,s,u,o;let d=await w(e,Object.assign(Object.assign({},m),{headers:y,signal:p.signal}));await T(d),await r(d.body,(i=function(e,t,n){let r=a(),s=new TextDecoder;return function(i,l){if(0===i.length)null==n||n(r),r=a();else if(l>0){let n=s.decode(i.subarray(0,l)),a=l+(32===i[l+1]?2:1),u=s.decode(i.subarray(a));switch(n){case"data":r.data=r.data?r.data+"\n"+u:u;break;case"event":r.event=u;break;case"id":e(r.id=u);break;case"retry":let o=parseInt(u,10);isNaN(o)||t(r.retry=o)}}}}(e=>{e?y[l]=e:delete y[l]},e=>{g=e},c),o=!1,function(e){void 0===n?(n=e,s=0,u=-1):n=function(e,t){let n=new Uint8Array(e.length+t.length);return n.set(e),n.set(t,e.length),n}(n,e);let t=n.length,r=0;for(;s<t;){o&&(10===n[s]&&(r=++s),o=!1);let e=-1;for(;s<t&&-1===e;++s)switch(n[s]){case 58:-1===u&&(u=s-r);break;case 13:o=!0;case 10:e=s}if(-1===e)break;i(n.subarray(r,e),u),r=s,u=-1}r===t?n=void 0:0!==r&&(n=n.subarray(r),s-=r)})),null==f||f(),E(),t()}catch(e){if(!p.signal.aborted)try{let t=null!==(n=null==b?void 0:b(e))&&void 0!==n?n:g;window.clearTimeout(N),N=window.setTimeout(k,t)}catch(e){E(),s(e)}}}k()})}function o(e){let t=e.headers.get("content-type");if(!(null==t?void 0:t.startsWith(i)))throw Error(`Expected content-type to be ${i}, Actual: ${t}`)}},61158:function(e,t,n){n.d(t,{W:function(){return a}});var r=n(2265);function a(e){return r.Children.toArray(e).filter(e=>(0,r.isValidElement)(e))}},27771:function(e,t,n){n.d(t,{T:function(){return s}});var r=n(2265),a=n(37977);function s(e){let{value:t,defaultValue:n,onChange:s,shouldUpdate:i=(e,t)=>e!==t}=e,l=(0,a.W)(s),u=(0,a.W)(i),[o,d]=(0,r.useState)(n),c=void 0!==t,f=c?t:o,b=(0,a.W)(e=>{let t="function"==typeof e?e(f):e;u(f,t)&&(c||d(t),l(t))},[c,l,f,u]);return[f,b]}},22043:function(e,t,n){n.d(t,{h:function(){return l}});var r=n(10056),a=n(58250),s=n(82184),i=n(57437),l=(0,a.G)((e,t)=>{let n=(0,r.p)();return(0,i.jsx)(s.m.thead,{...e,ref:t,__css:n.thead})})},10056:function(e,t,n){n.d(t,{i:function(){return f},p:function(){return c}});var r=n(58250),a=n(89839),s=n(50446),i=n(82184),l=n(16465),u=n(310),o=n(57437),[d,c]=(0,u.k)({name:"TableStylesContext",errorMessage:"useTableStyles returned is 'undefined'. Seems you forgot to wrap the components in \"<Table />\" "}),f=(0,r.G)((e,t)=>{let n=(0,a.jC)("Table",e),{className:r,layout:u,...c}=(0,s.Lr)(e);return(0,o.jsx)(d,{value:n,children:(0,o.jsx)(i.m.table,{ref:t,__css:{tableLayout:u,...n.table},className:(0,l.cx)("chakra-table",r),...c})})});f.displayName="Table"},52736:function(e,t,n){n.d(t,{Tr:function(){return l}});var r=n(10056),a=n(58250),s=n(82184),i=n(57437),l=(0,a.G)((e,t)=>{let n=(0,r.p)();return(0,i.jsx)(s.m.tr,{...e,ref:t,__css:n.tr})})},97464:function(e,t,n){n.d(t,{p:function(){return l}});var r=n(10056),a=n(58250),s=n(82184),i=n(57437),l=(0,a.G)((e,t)=>{let n=(0,r.p)();return(0,i.jsx)(s.m.tbody,{...e,ref:t,__css:n.tbody})})},17885:function(e,t,n){n.d(t,{Th:function(){return l}});var r=n(10056),a=n(58250),s=n(82184),i=n(57437),l=(0,a.G)(({isNumeric:e,...t},n)=>{let a=(0,r.p)();return(0,i.jsx)(s.m.th,{...t,ref:n,__css:a.th,"data-is-numeric":e})})},15982:function(e,t,n){n.d(t,{x:function(){return l}});var r=n(58250),a=n(82184),s=n(16465),i=n(57437),l=(0,r.G)((e,t)=>{var n;let{overflow:r,overflowX:l,className:u,...o}=e;return(0,i.jsx)(a.m.div,{ref:t,className:(0,s.cx)("chakra-table__container",u),...o,__css:{display:"block",whiteSpace:"nowrap",WebkitOverflowScrolling:"touch",overflowX:null!=(n=null!=r?r:l)?n:"auto",overflowY:"hidden",maxWidth:"100%"}})})},32527:function(e,t,n){n.d(t,{Td:function(){return l}});var r=n(10056),a=n(58250),s=n(82184),i=n(57437),l=(0,a.G)(({isNumeric:e,...t},n)=>{let a=(0,r.p)();return(0,i.jsx)(s.m.td,{...t,ref:n,__css:a.td,"data-is-numeric":e})})},98386:function(e,t,n){n.d(t,{t:function(){return o}});var r=n(51791),a=n(90024),s=n(16465),i=n(58250),l=n(82184),u=n(57437),o=(0,i.G)(function(e,t){let n=(0,a.hp)({...e,ref:t}),i={display:"flex",...(0,r.s)().tablist};return(0,u.jsx)(l.m.div,{...n,className:(0,s.cx)("chakra-tabs__tablist",e.className),__css:i})});o.displayName="TabList"},51791:function(e,t,n){n.d(t,{m:function(){return h},s:function(){return b}});var r=n(90024),a=n(310),s=n(58250),i=n(89839),l=n(50446),u=n(82184),o=n(16465),d=n(2265),c=n(57437),[f,b]=(0,a.k)({name:"TabsStylesContext",errorMessage:"useTabsStyles returned is 'undefined'. Seems you forgot to wrap the components in \"<Tabs />\" "}),h=(0,s.G)(function(e,t){let n=(0,i.jC)("Tabs",e),{children:a,className:s,...b}=(0,l.Lr)(e),{htmlProps:h,descendants:v,...m}=(0,r.YE)(b),p=(0,d.useMemo)(()=>m,[m]),{isFitted:y,...x}=h,g={position:"relative",...n.root};return(0,c.jsx)(r.mE,{value:v,children:(0,c.jsx)(r.X,{value:p,children:(0,c.jsx)(f,{value:n,children:(0,c.jsx)(u.m.div,{className:(0,o.cx)("chakra-tabs",s),ref:t,...x,__css:g,children:a})})})})});h.displayName="Tabs"},93628:function(e,t,n){n.d(t,{O:function(){return o}});var r=n(51791),a=n(90024),s=n(16465),i=n(58250),l=n(82184),u=n(57437),o=(0,i.G)(function(e,t){let n=(0,r.s)(),i=(0,a.xD)({...e,ref:t}),o={outline:"0",display:"flex",alignItems:"center",justifyContent:"center",...n.tab};return(0,u.jsx)(l.m.button,{...i,className:(0,s.cx)("chakra-tabs__tab",e.className),__css:o})});o.displayName="Tab"},90024:function(e,t,n){n.d(t,{mE:function(){return E},X:function(){return C},xD:function(){return D},hp:function(){return _},WE:function(){return M},bt:function(){return P},YE:function(){return O}});var r=n(2265),a=n(16465),s=n(45663);function i(e){let{tagName:t,isContentEditable:n}=e.target;return"INPUT"!==t&&"TEXTAREA"!==t&&!0!==n}var l=Object.defineProperty,u=(e,t,n)=>t in e?l(e,t,{enumerable:!0,configurable:!0,writable:!0,value:n}):e[t]=n,o=(e,t,n)=>(u(e,"symbol"!=typeof t?t+"":t,n),n);function d(e){return e.sort((e,t)=>{let n=e.compareDocumentPosition(t);if(n&Node.DOCUMENT_POSITION_FOLLOWING||n&Node.DOCUMENT_POSITION_CONTAINED_BY)return -1;if(n&Node.DOCUMENT_POSITION_PRECEDING||n&Node.DOCUMENT_POSITION_CONTAINS)return 1;if(!(n&Node.DOCUMENT_POSITION_DISCONNECTED)&&!(n&Node.DOCUMENT_POSITION_IMPLEMENTATION_SPECIFIC))return 0;throw Error("Cannot sort the given nodes.")})}var c=e=>"object"==typeof e&&"nodeType"in e&&e.nodeType===Node.ELEMENT_NODE;function f(e,t,n){let r=e+1;return n&&r>=t&&(r=0),r}function b(e,t,n){let r=e-1;return n&&r<0&&(r=t),r}var h="undefined"!=typeof window?r.useLayoutEffect:r.useEffect,v=e=>e,m=class{constructor(){o(this,"descendants",new Map),o(this,"register",e=>{if(null!=e)return c(e)?this.registerNode(e):t=>{this.registerNode(t,e)}}),o(this,"unregister",e=>{this.descendants.delete(e);let t=d(Array.from(this.descendants.keys()));this.assignIndex(t)}),o(this,"destroy",()=>{this.descendants.clear()}),o(this,"assignIndex",e=>{this.descendants.forEach(t=>{let n=e.indexOf(t.node);t.index=n,t.node.dataset.index=t.index.toString()})}),o(this,"count",()=>this.descendants.size),o(this,"enabledCount",()=>this.enabledValues().length),o(this,"values",()=>Array.from(this.descendants.values()).sort((e,t)=>e.index-t.index)),o(this,"enabledValues",()=>this.values().filter(e=>!e.disabled)),o(this,"item",e=>{if(0!==this.count())return this.values()[e]}),o(this,"enabledItem",e=>{if(0!==this.enabledCount())return this.enabledValues()[e]}),o(this,"first",()=>this.item(0)),o(this,"firstEnabled",()=>this.enabledItem(0)),o(this,"last",()=>this.item(this.descendants.size-1)),o(this,"lastEnabled",()=>{let e=this.enabledValues().length-1;return this.enabledItem(e)}),o(this,"indexOf",e=>{var t,n;return e&&null!=(n=null==(t=this.descendants.get(e))?void 0:t.index)?n:-1}),o(this,"enabledIndexOf",e=>null==e?-1:this.enabledValues().findIndex(t=>t.node.isSameNode(e))),o(this,"next",(e,t=!0)=>{let n=f(e,this.count(),t);return this.item(n)}),o(this,"nextEnabled",(e,t=!0)=>{let n=this.item(e);if(!n)return;let r=f(this.enabledIndexOf(n.node),this.enabledCount(),t);return this.enabledItem(r)}),o(this,"prev",(e,t=!0)=>{let n=b(e,this.count()-1,t);return this.item(n)}),o(this,"prevEnabled",(e,t=!0)=>{let n=this.item(e);if(!n)return;let r=b(this.enabledIndexOf(n.node),this.enabledCount()-1,t);return this.enabledItem(r)}),o(this,"registerNode",(e,t)=>{if(!e||this.descendants.has(e))return;let n=d(Array.from(this.descendants.keys()).concat(e));(null==t?void 0:t.disabled)&&(t.disabled=!!t.disabled);let r={node:e,index:-1,...t};this.descendants.set(e,r),this.assignIndex(n)})}},p=n(310),[y,x]=(0,p.k)({name:"DescendantsProvider",errorMessage:"useDescendantsContext must be used within DescendantsProvider"}),g=n(27771),N=n(61158),[E,w,T,k]=[v(y),()=>v(x()),()=>(function(){let e=(0,r.useRef)(new m);return h(()=>()=>e.current.destroy()),e.current})(),e=>(function(e){let t=x(),[n,a]=(0,r.useState)(-1),i=(0,r.useRef)(null);h(()=>()=>{i.current&&t.unregister(i.current)},[]),h(()=>{if(!i.current)return;let e=Number(i.current.dataset.index);n==e||Number.isNaN(e)||a(e)});let l=e?v(t.register(e)):v(t.register);return{descendants:t,index:n,enabledIndex:t.enabledIndexOf(i.current),register:(0,s.lq)(l,i)}})(e)];function O(e){var t;let{defaultIndex:n,onChange:a,index:s,isManual:i,isLazy:l,lazyBehavior:u="unmount",orientation:o="horizontal",direction:d="ltr",...c}=e,[f,b]=(0,r.useState)(null!=n?n:0),[h,v]=(0,g.T)({defaultValue:null!=n?n:0,value:s,onChange:a});(0,r.useEffect)(()=>{null!=s&&b(s)},[s]);let m=T(),p=(0,r.useId)(),y=null!=(t=e.id)?t:p;return{id:`tabs-${y}`,selectedIndex:h,focusedIndex:f,setSelectedIndex:v,setFocusedIndex:b,isManual:i,isLazy:l,lazyBehavior:u,orientation:o,descendants:m,direction:d,htmlProps:c}}var[C,I]=(0,p.k)({name:"TabsContext",errorMessage:"useTabsContext: `context` is undefined. Seems you forgot to wrap all tabs components within <Tabs />"});function _(e){let{focusedIndex:t,orientation:n,direction:s}=I(),i=w(),l=(0,r.useCallback)(e=>{let r=()=>{var e;let n=i.nextEnabled(t);n&&(null==(e=n.node)||e.focus())},a=()=>{var e;let n=i.prevEnabled(t);n&&(null==(e=n.node)||e.focus())},l="horizontal"===n,u="vertical"===n,o={["ltr"===s?"ArrowLeft":"ArrowRight"]:()=>l&&a(),["ltr"===s?"ArrowRight":"ArrowLeft"]:()=>l&&r(),ArrowDown:()=>u&&r(),ArrowUp:()=>u&&a(),Home:()=>{var e;let t=i.firstEnabled();t&&(null==(e=t.node)||e.focus())},End:()=>{var e;let t=i.lastEnabled();t&&(null==(e=t.node)||e.focus())}}[e.key];o&&(e.preventDefault(),o(e))},[i,t,n,s]);return{...e,role:"tablist","aria-orientation":n,onKeyDown:(0,a.v0)(e.onKeyDown,l)}}function D(e){let{isDisabled:t=!1,isFocusable:n=!1,...l}=e,{setSelectedIndex:u,isManual:o,id:d,setFocusedIndex:c,selectedIndex:f}=I(),{index:b,register:h}=k({disabled:t&&!n}),v=b===f;return{...function(e={}){let{ref:t,isDisabled:n,isFocusable:l,clickOnEnter:u=!0,clickOnSpace:o=!0,onMouseDown:d,onMouseUp:c,onClick:f,onKeyDown:b,onKeyUp:h,tabIndex:v,onMouseOver:m,onMouseLeave:p,...y}=e,[x,g]=(0,r.useState)(!0),[N,E]=(0,r.useState)(!1),w=function(){let e=(0,r.useRef)(new Map),t=e.current,n=(0,r.useCallback)((t,n,r,a)=>{e.current.set(r,{type:n,el:t,options:a}),t.addEventListener(n,r,a)},[]),a=(0,r.useCallback)((t,n,r,a)=>{t.removeEventListener(n,r,a),e.current.delete(r)},[]);return(0,r.useEffect)(()=>()=>{t.forEach((e,t)=>{a(e.el,e.type,t,e.options)})},[a,t]),{add:n,remove:a}}(),T=x?v:v||0,k=n&&!l,O=(0,r.useCallback)(e=>{if(n){e.stopPropagation(),e.preventDefault();return}e.currentTarget.focus(),null==f||f(e)},[n,f]),C=(0,r.useCallback)(e=>{N&&i(e)&&(e.preventDefault(),e.stopPropagation(),E(!1),w.remove(document,"keyup",C,!1))},[N,w]),I=(0,r.useCallback)(e=>{if(null==b||b(e),n||e.defaultPrevented||e.metaKey||!i(e.nativeEvent)||x)return;let t=u&&"Enter"===e.key;o&&" "===e.key&&(e.preventDefault(),E(!0)),t&&(e.preventDefault(),e.currentTarget.click()),w.add(document,"keyup",C,!1)},[n,x,b,u,o,w,C]),_=(0,r.useCallback)(e=>{null==h||h(e),!n&&!e.defaultPrevented&&!e.metaKey&&i(e.nativeEvent)&&!x&&o&&" "===e.key&&(e.preventDefault(),E(!1),e.currentTarget.click())},[o,x,n,h]),D=(0,r.useCallback)(e=>{0===e.button&&(E(!1),w.remove(document,"mouseup",D,!1))},[w]),S=(0,r.useCallback)(e=>{if(0===e.button){if(n){e.stopPropagation(),e.preventDefault();return}x||E(!0),e.currentTarget.focus({preventScroll:!0}),w.add(document,"mouseup",D,!1),null==d||d(e)}},[n,x,d,w,D]),j=(0,r.useCallback)(e=>{0===e.button&&(x||E(!1),null==c||c(e))},[c,x]),P=(0,r.useCallback)(e=>{if(n){e.preventDefault();return}null==m||m(e)},[n,m]),M=(0,r.useCallback)(e=>{N&&(e.preventDefault(),E(!1)),null==p||p(e)},[N,p]),A=(0,s.lq)(t,e=>{e&&"BUTTON"!==e.tagName&&g(!1)});return x?{...y,ref:A,type:"button","aria-disabled":k?void 0:n,disabled:k,onClick:O,onMouseDown:d,onMouseUp:c,onKeyUp:h,onKeyDown:b,onMouseOver:m,onMouseLeave:p}:{...y,ref:A,role:"button","data-active":(0,a.PB)(N),"aria-disabled":n?"true":void 0,tabIndex:k?void 0:T,onClick:O,onMouseDown:S,onMouseUp:j,onKeyUp:_,onKeyDown:I,onMouseOver:P,onMouseLeave:M}}({...l,ref:(0,s.lq)(h,e.ref),isDisabled:t,isFocusable:n,onClick:(0,a.v0)(e.onClick,()=>{u(b)})}),id:A(d,b),role:"tab",tabIndex:v?0:-1,type:"button","aria-selected":v,"aria-controls":L(d,b),onFocus:t?void 0:(0,a.v0)(e.onFocus,()=>{c(b);let e=t&&n;o||e||u(b)})}}var[S,j]=(0,p.k)({});function P(e){let{id:t,selectedIndex:n}=I(),a=(0,N.W)(e.children).map((e,a)=>(0,r.createElement)(S,{key:a,value:{isSelected:a===n,id:L(t,a),tabId:A(t,a),selectedIndex:n}},e));return{...e,children:a}}function M(e){let{children:t,...n}=e,{isLazy:a,lazyBehavior:s}=I(),{isSelected:i,id:l,tabId:u}=j(),o=(0,r.useRef)(!1);i&&(o.current=!0);let d=function(e){let{wasSelected:t,enabled:n,isSelected:r,mode:a="unmount"}=e;return!n||!!r||"keepMounted"===a&&!!t}({wasSelected:o.current,isSelected:i,enabled:a,mode:s});return{tabIndex:0,...n,children:d?t:null,role:"tabpanel","aria-labelledby":u,hidden:!i,id:l}}function A(e,t){return`${e}--tab-${t}`}function L(e,t){return`${e}--tabpanel-${t}`}}}]);