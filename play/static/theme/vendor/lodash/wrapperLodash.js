var LazyWrapper=require("./_LazyWrapper"),LodashWrapper=require("./_LodashWrapper"),baseLodash=require("./_baseLodash"),isArray=require("./isArray"),isObjectLike=require("./isObjectLike"),wrapperClone=require("./_wrapperClone"),objectProto=Object.prototype,hasOwnProperty=objectProto.hasOwnProperty;function lodash(r){if(isObjectLike(r)&&!isArray(r)&&!(r instanceof LazyWrapper)){if(r instanceof LodashWrapper)return r;if(hasOwnProperty.call(r,"__wrapped__"))return wrapperClone(r)}return new LodashWrapper(r)}lodash.prototype=baseLodash.prototype,lodash.prototype.constructor=lodash,module.exports=lodash;