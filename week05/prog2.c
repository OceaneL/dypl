#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdarg.h>


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
  struct _ClassNext * classNext;
  Method* firstMethod;
  char* name;
} Class;

typedef struct _ClassNext {
  struct _Class * class;
  struct _ClassNext * next;
  int hasBeenRemove;
} ClassNext;

int containsInTail(Class * c, ClassNext* list ){
  ClassNext *  e = list;
  int first = 1;
  while (e != NULL) {
    if (!first) {
      if (e->class == c && !e->hasBeenRemove){
        return 1;
      }
    }
    else first = 0;
    e = e->next;
  }
  return 0;
}

void removeList (Class * c, ClassNext* list ){
  ClassNext *  e = list;
  while (e != NULL) {
    if (e->class == c && !e->hasBeenRemove)
      e->hasBeenRemove = 1;
    e = e->next;
  }
}

int isEmpty (ClassNext* list ){
  ClassNext * e = list;
  while (e != NULL) {
    if (!e->hasBeenRemove)
      return 0;
    e = e->next;
  }
  return 1;
}

Class * firstClass (ClassNext* list ){
  ClassNext * e = list;
  while (e != NULL) {
    if (!e->hasBeenRemove)
      return e->class;
    e = e->next;
  }
  return NULL;
}

void initialize (ClassNext* list ){
  ClassNext * e = list;
  while (e != NULL) {
    e->hasBeenRemove = 0;
    e = e->next;
  }
}



typedef struct _Object {
  Class* class;
  char* msg;
} Object;


void merge(int n, ClassNext ** list, Class ** classes)
{
  int ind = 1; //compteur remplissage classes
   int k;
   for (k = 0; k < n; k++)
   {
     printf("k = %d\n",k );
      initialize(list[k]);
   }

   int isEmpty2 = 0;
   int ok;
   while (!isEmpty2){
     int i;
     for (i = 0; i < n; i++)
     {
        Class * class = firstClass(list[i]);
        int j;
        ok = 1;
        for (j = 0; j < n; j++)
        {
          if (containsInTail(class, list[i])){
            ok = 0;
          }
        }
        if (ok){
          for (int p = 0; p < n; p++) {
            removeList(class, list[p]);
          }
          classes[i] = class;
          ind++;
          break;
        }
     }
     isEmpty2 = 1;
     for (int p = 0; p < n; p++) {
       isEmpty2 &= isEmpty(list[p]);
     }
     if (!ok){
       printf("ambiguous inheritance\n");
       exit(EXIT_FAILURE);
     }
   }
}

void configureHeritance(Class * class, int n, ...)
{
   va_list va;
   va_start (va, n);

   int i;
   Class ** list;
   list = (Class **) malloc((n+1) * sizeof(Class *));
   ClassNext ** listClassNext = malloc((n+1) * sizeof(ClassNext *));
   list[n] = class;
   for (i = 0; i < n; i++){
    list[n-i-1] = va_arg (va, Class*);
    listClassNext[i] = list[n-i-1]->classNext;
    printf("1 %s\n",list[n-i-1]->classNext->class->name );
   }
   ClassNext * cni = NULL;
   for (i = 0; i < n; i++){
     ClassNext cn;
     cn.class = list[i];
     initialize(listClassNext[0]);
     cn.next =cni;
     cni = &cn;
     initialize(listClassNext[0]);
   }
   va_end (va);
   listClassNext[n]= cni;
   Class * classes[n+1];
   merge(n+1,listClassNext, classes);
   classes[0]= class;
   ClassNext * cni2 = NULL;
   for (int i = n; i >= 0; i--) {
     ClassNext cn;
     cn.class = classes[i];
     cn.next =cni2;
     cni2 = &cn;
   }
   class->classNext=cni2;
}


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
  ClassNext * class = object->class->classNext;
  Method * method = NULL;
  while ((class != NULL) && ((method = findMethod(class->class->firstMethod, methodname, argnum)) == NULL )) {
    class = class->next;
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
  class.name= "A";
  configureHeritance(&class, 0);
  class.firstMethod = &method;
  Class subClass;
  subClass.name ="B";
  configureHeritance(&subClass, 1, &class );
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
