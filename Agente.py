import clips

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

sistemaExperto = clips.Environment()
sistemaExperto.clear()

gFinanciacion = ctrl.Antecedent(np.arange(0, 5, 0.1), 'gFinanciacion')
tPlantilla = ctrl.Antecedent(np.arange(0, 10, 0.1), 'tPlantilla')
rFinanciacion = ctrl.Consequent(np.arange(0, 5, 0.5), 'rFinanciacion')

gFinanciacion['pobre']=fuzz.trapmf(gFinanciacion.universe,[0,0,1,1.6])
gFinanciacion['bueno']=fuzz.trapmf(gFinanciacion.universe,[1.4,2.6,3.2,3.5])
gFinanciacion['excelente']=fuzz.trapmf(gFinanciacion.universe,[3.7,4.3,5,5])

tPlantilla['mala']=fuzz.trapmf(tPlantilla.universe,[0,0,4,5])
tPlantilla['normal']=fuzz.trapmf(tPlantilla.universe,[4,6,7,8])
tPlantilla['efectiva']=fuzz.trapmf(tPlantilla.universe,[6.9,9,10,10])

rFinanciacion['bajo'] = fuzz.trimf(rFinanciacion.universe, [0, 0, 1.9])
rFinanciacion['medio'] = fuzz.trimf(rFinanciacion.universe, [1.7, 3.1, 4])
rFinanciacion['alto'] = fuzz.trimf(rFinanciacion.universe, [3.6, 5, 5])

for t in gFinanciacion.terms.values():
    print(t.label)
    
for t in tPlantilla.terms.values():
    print(t.label)

for t in rFinanciacion.terms.values():
    print(t.label)

alto = ctrl.Rule(gFinanciacion['pobre'] & tPlantilla['mala'], rFinanciacion['alto'])
medio = ctrl.Rule(gFinanciacion['bueno'] & tPlantilla['efectiva'], rFinanciacion['medio'])
bajo = ctrl.Rule(gFinanciacion['excelente'] & tPlantilla['efectiva'], rFinanciacion['bajo'])

riesgo_ctrl = ctrl.ControlSystem([alto,medio, bajo])
riesgo = ctrl.ControlSystemSimulation(riesgo_ctrl)

for regla in riesgo_ctrl.rules:
  print (regla.antecedent," --> ",regla.consequent)
  
Financiacion=5
Plantilla=8
riesgo.input['gFinanciacion'] = Financiacion
riesgo.input['tPlantilla'] = Plantilla
riesgo.compute()
resultado=riesgo.output['rFinanciacion']
print ("Nivel del riesgo ",resultado)
riesgo = ''
if resultado >= 0 or resultado <= 0.4:
    riesgo = 'alto'
elif resultado >= 0.41 | resultado <= 0.69:
    riesgo = 'medio'
else:
    riesgo = 'bajo'

deftemplate_ROI_Riesgo = ("(deftemplate proyecto (slot nombre (type STRING)) (slot ROI (type INTEGER)) (slot riesgo (type SYMBOL)))")

defHechos = (f'(proyecto(nombre "Proyecto A") (ROI 30) (riesgo {riesgo}))')

defRule_Aceptado = ('(defrule AceptarProyecto (proyecto (nombre ?nombre) (ROI ?roi&:(>= ?roi 15)) (riesgo bajo|medio)) => (assert(Aceptado)))')
defRule_rechazado_roi = ('(defrule rechazar-proyecto-por-roi (proyecto (nombre ?nombre) (ROI ?roi&:(< ?roi 15)) (riesgo medio|alto)) => (assert(proyectoRechazado_roi)))')
defRule_rechazado_riesgo = ('(defrule rechazar-proyecto-por-riesgo (proyecto (nombre ?nombre) (ROI ?roi&:(>= ?roi 15)) (riesgo alto)) => (assert(proyectoRechazado_riesgo)))')
defRule_rechazado_roi_riesgo = ('(defrule rechazar-proyecto-por-todo (proyecto (nombre ?nombre) (ROI ?roi&:(< ?roi 15)) (riesgo alto)) => (assert(proyectoRechazado_roi_riesgo)))')
sistemaExperto.build(deftemplate_ROI_Riesgo)
sistemaExperto.build(defRule_Aceptado)
sistemaExperto.build(defRule_rechazado_roi)
sistemaExperto.build(defRule_rechazado_riesgo)
sistemaExperto.build(defRule_rechazado_roi_riesgo)
sistemaExperto.assert_string(defHechos)


for r in sistemaExperto.rules():
  print(r)

#sistemaExperto.assert_string("(deffacts proyectos(proyecto (nombre Proyecto A) (ROI 20) (gFinanciacion 2.3) (tPlantilla 5) (rFinanciacion 3)))")


for fact in sistemaExperto.facts():
  print(fact)

for ac in sistemaExperto.activations():
  print(ac)

sistemaExperto.run()



