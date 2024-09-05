import clips
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from tkinter import *


def expertDifuso():
    sistemaExperto = clips.Environment()
    sistemaExperto.clear()

    gFinanciacion = ctrl.Antecedent(np.arange(0, 5, 0.1), 'gFinanciacion')
    tPlantilla = ctrl.Antecedent(np.arange(0, 5, 0.1), 'tPlantilla')
    rFinanciacion = ctrl.Consequent(np.arange(0, 5, 0.1), 'rFinanciacion')

    gFinanciacion['pobre']=fuzz.trapmf(gFinanciacion.universe,[0,0,1,1.9])
    gFinanciacion['bueno']=fuzz.trapmf(gFinanciacion.universe,[1.4,2.6,3.2,3.9])
    gFinanciacion['excelente']=fuzz.trapmf(gFinanciacion.universe,[3.1,4.3,5,5])

    tPlantilla['mala']=fuzz.trapmf(tPlantilla.universe,[0,0,2,2.9])
    tPlantilla['normal']=fuzz.trapmf(tPlantilla.universe,[2.5,3,3.5,3.9])
    tPlantilla['efectiva']=fuzz.trapmf(tPlantilla.universe,[3.5,4,5,5])

    rFinanciacion['bajo'] = fuzz.trimf(rFinanciacion.universe, [0, 0, 1.9])
    rFinanciacion['medio'] = fuzz.trimf(rFinanciacion.universe, [1.7, 3.1, 4])
    rFinanciacion['alto'] = fuzz.trimf(rFinanciacion.universe, [3.6, 5, 5])

    for t in gFinanciacion.terms.values():
        print(t.label)
        
    for t in tPlantilla.terms.values():
        print(t.label)

    for t in rFinanciacion.terms.values():
        print(t.label)
        
    gFinanciacion.view()
    tPlantilla.view()
    rFinanciacion.view()

    alto = ctrl.Rule(gFinanciacion['pobre'] & tPlantilla['mala'], rFinanciacion['alto'])
    medio = ctrl.Rule(gFinanciacion['bueno'] & tPlantilla['efectiva'], rFinanciacion['medio'])
    bajo = ctrl.Rule(gFinanciacion['excelente'] & tPlantilla['efectiva'], rFinanciacion['bajo'])

    riesgo_ctrl = ctrl.ControlSystem([bajo,medio, alto])
    riesgo = ctrl.ControlSystemSimulation(riesgo_ctrl)

    for regla in riesgo_ctrl.rules:
        print(regla.antecedent," --> ",regla.consequent)
    numero1 = txtFinanciero.get()
    numero1 = float(numero1)
    print(type(numero1))
    numero2 = txtPlantilla.get()
    numero2 = float(numero2)
    print(type(numero2))
    riesgo.input['gFinanciacion'] = numero1
    riesgo.input['tPlantilla'] = numero2
    riesgo.compute()
    resultado=riesgo.output['rFinanciacion']
   
    print ("Nivel del riesgo ",resultado)
    rFinanciacion.view(sim=riesgo)
    plt.show()
    riesgo = ''
    if resultado <= 1.8:
        riesgo = 'bajo'
    elif resultado <= 3.9:
        riesgo = 'medio'
    else:
        riesgo = 'alto'

    print(f"**********RIESGO: {riesgo}******************")
    ##SISTEMA EXPERTO  
    deftemplate_ROI_Riesgo = ("(deftemplate proyecto (slot nombre (type STRING)) (slot ROI (type INTEGER)) (slot riesgo (type SYMBOL)))")

    defHechos = (f'(proyecto(nombre "{txtProyecto.get()}") (ROI {int(txtROI.get())}) (riesgo {riesgo}))')

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
    for fact in sistemaExperto.facts():
        print(fact)
    for ac in sistemaExperto.activations():
        print(ac)
        lblResult.configure(text = ac)
    sistemaExperto.run()



root = Tk()
root.title("Sistama experto y logica difusa")
root.geometry('350x200')


lblProyecto = Label(root, text = "ingrese nombre del proyecto")
lblProyecto.grid()
txtProyecto = Entry(root, width=15)
txtProyecto.grid(column =1, row =0)

lblgFinanciero = Label(root, text = "ingrese valor gastos financieros")
lblgFinanciero.grid()
txtFinanciero = Entry(root, width=15)
txtFinanciero.grid(column =1, row =1)


lblPlantilla = Label(root, text = "ingrese valor plantilla")
lblPlantilla.grid()
txtPlantilla = Entry(root, width=15)
txtPlantilla.grid(column =1, row =2)


lblROI = Label(root, text = "ingrese valor ROI")
lblROI.grid()
txtROI = Entry(root, width=15)
txtROI.grid(column =1, row =3)

lblResult = Label(root, text = "")
lblResult.grid(column=1, row=5)

btn = Button(root, text = "Iniciar" , fg = "black", command=expertDifuso)
# Set Button Grid
btn.grid(column=1, row=6)

root.mainloop()
