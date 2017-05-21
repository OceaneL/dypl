#include <stdio.h>
#include <string.h>
#include <stdlib.h>


typedef struct _Method {
  void * method;
  char * name;
  int argnum;
  struct _Method * next;
} Method;

Method * findMethod(Method * method, char* name, int argnum){
  while( (method != NULL) &&((strcmp(method->name, name) != 0) || method->argnum != argnum ) ) {
    method = method->next;
  }
  return method;
}

typedef struct _Class {
  struct _Class * super;
  Method* firstMethod;
} Class;

typedef struct _Object {
  Class* class;
  char* msg;
} Object;
void * printMsg(Object* self){
  puts(self->msg);
  return NULL;
}

void * printHello(Object* self){
  puts("hello");
  return NULL;
}

void * printMsgSubClass(Object* self){
  puts("in the subclass");
  return NULL;
}
void * setMsg(Object* self, void* msg){
  self->msg = (char *)msg;
  return NULL;
}

void* invoke(void* receiver, char* methodname,
int argnum, void* argvalue){
  Object * object = (Object*) receiver;
  Class * class = object->class;
  Method * method = NULL;
  while ((class != NULL) && ((method = findMethod(class->firstMethod, methodname, argnum)) == NULL )) {
    class = class->super;
  }
  if (method == NULL){
    printf("methode %s non definie\n", methodname);
    exit (EXIT_FAILURE);
  }
  void * result = NULL;
  if (argnum == 0){
    void * (*f)(Object *);
    f = method->method;
    result = (*f) (object);
  }
  else{
    void * (*f)(Object *, void *);
    f = method->method;
    result = (*f) (object, argvalue);
  }
  return result;
}
int main(void){
  Method method3;
  method3.method = (void *) printHello;
  method3.name = "printHello";
  method3.argnum = 0;
  method3.next = NULL;
  Method method2;
  method2.method = (void *) setMsg;
  method2.name = "setMsg";
  method2.argnum = 1;
  method2.next = &method3;
  Method method;
  method.method = (void *) printMsg;
  method.name = "printMsg";
  method.argnum = 0;
  method.next = &method2;
  Method methodSub;
  methodSub.method = (void *) printMsgSubClass;
  methodSub.name = "printMsg";
  methodSub.argnum = 0;
  methodSub.next = NULL;
  Class class;
  class.super = NULL;
  class.firstMethod = &method;
  Class subClass;
  subClass.super = &class;
  subClass.firstMethod = &methodSub;
  Object obj;
  obj.class = &class;
  Object obj2;
  obj2.class = &subClass;
  /* Now the important part */
  invoke(&obj, "setMsg", 1, "Hello, world");
  invoke(&obj, "printMsg", 0, NULL);
  invoke(&obj, "setMsg", 1, "This is another message");
  invoke(&obj, "printMsg", 0, NULL);
  invoke(&obj2, "printMsg", 0, NULL);
  invoke(&obj2, "printHello", 0, NULL);
  return 0;
}
