var assocIndexOf=require("./_assocIndexOf"),arrayProto=Array.prototype,splice=arrayProto.splice;function listCacheDelete(e){var r=this.__data__,a=assocIndexOf(r,e);return!(a<0)&&(a==r.length-1?r.pop():splice.call(r,a,1),--this.size,!0)}module.exports=listCacheDelete;