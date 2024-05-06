import gpt_wrapper
from gpt_wrapper.chat import Chat
from IPython import display
from tqdm import tqdm

gpt_wrapper.api_key = "fc8f2ffd-9b78-401e-a77d-162512bb597c"

import json
path = "data/47.json"

def load_data():
    with open(path) as f :
        data = json.load(f)
    return data

def save_data(path, data):
    with open(path) as f:
        json.dump(data, f)

class GPTQuerier:
    
    def __init__(self, level):
        self.session_id = 0
    
        self.prompt_simpleQ = """You a teacher in an insitute of technology.
        Your goal is to answer student's question and help them understand the answer. It needs to be very clear.
        Your answers shouldn't assume anything more than what's stated in the question.
        Describe the reasoning that lead you to this conclusion with a solid argument (when you are sure about it)."""
    
        if(level == 0):
            self.instruction_prompt = """You a teacher in an insitute of technology.
            Your goal is to answer student's question and help them understand the answer. It needs to be very clear.
            Your answers shouldn't assume anything more than what's stated in the question. A True asnwers is always right, if you can find a condition for which the proposition is not true, then it's false.
            For each of the possible answer state if they are True of False and for each describe the reasoning that lead you to this conclusion with a solid argument (when you are sure about it).
            You will do a list stating the index of the answer, what the proposed answer was and your thoughts about it
            """
        elif(level == 1):
            self.instruction_prompt = """

            You are a teacher in an Institure of technology. Your goal is to provide correct and well explained answer so that your
            student can learn from your explaination. 

            You'll have a question and multiple proposed answers. You will list all the answers in the order they were proposed and 
            for each of them you will give the answers and a chain of thoughts as described in the NeurIPS paper "Chain-of-Thought Prompting Elicits Reasoning
            in Large Language Models". Your answer should provide all the steps of reasoning so that the student will
            fully understand the answer. 

            In a multiple choice question, a propostion is considered true when we can't find any counter example. It has to be true all the time.

            You will finish by simply stating what the answer was.
            """
        
        elif(level == 2):
            self.instruction_prompt = """

            You are a teacher in an Institure of technology. Your goal is to provide correct and well explained answer so that your
            student can learn from your explaination. 

            Start by stating the definitions, lemmas, theorems, and formulas that are relevant to the resolution of the exercise.

            You'll have a question and multiple proposed answers. You will list all the answers in the order they were proposed and 
            for each of them you will give the answers and a chain of thoughts as described in the NeurIPS paper "Chain-of-Thought Prompting Elicits Reasoning
            in Large Language Models". Your answer should provide all the steps of reasoning so that the student will
            fully understand the answer. 

            In a multiple choice question, a propostion is considered true when we can't find any counter example. It has to be true all the time.

            You will finish by simply stating what the answer was.
            """
        elif(level == 2):
            self.instruction_prompt = """
            You are a teacher in an Institure of technology. Your goal is to provide correct and well explained answer so that your
            student can learn from your explaination. 

            Start by stating the definitions, lemmas, theorems, and formulas that are relevant to the resolution of the exercise.

            You'll have a question and multiple proposed answers. You will list all the answers in the order they were proposed. 
            For each of them you will you will proposed a reasoning justified by definitions and properties

            In a multiple choice question, a propostion is considered true when we can't find any counter example. It has to be true all the time.

            You will finish by simply stating what the answer was.
            """
        elif(level == 3):
            ## we try 2-shot prompting
            ## issue : the model can mimic the examples only when there are 4 possible answers.
            self.instruction_prompt = """
            You are a teacher in an Institure of technology. Your goal is to provide correct and well explained answer so that your
            student can learn from your explaination. 

            Start by stating the definitions, lemmas, theorems, and formulas that are relevant to the resolution of the exercise.

            You'll have a question and multiple proposed answers. You will list all the answers in the order they were proposed. 
            For each of them you will you will proposed a reasoning justified by definitions and properties

            In a multiple choice question, a propostion is considered true when we can't find any counter example. It has to be true all the time.

            You will finish by simply stating what the answer was.

            Here's an example of interactions :

            Q : 
                There is a multiple choice question with 4 possible solutions. Here is the question : Spatial localization in MRI primarily relies on.... Here is the answers : 1. "Distance to the receiving coil"  2. "Distance from the transmission coil"  3. "Varying magnetic field across the patient"  4. "Varying amplitude of RF pulse"  

            A : 
                To answer this question, we need to understand how spatial localization works in MRI. Spatial localization in MRI refers to the ability to determine where in the body a specific signal is coming from. This is important because MRI scans provide detailed images of the inside of the body, so knowing where a signal is coming from allows us to create clear images of specific areas.

                Answer 1, "Distance to the receiving coil" : False. The distance to the receiving coil does not play a direct role in spatial localization. The receiving coil is used to detect the signal that is emitted by the body, but it does not determine where that signal is coming from.

                Answer 2, "Distance from the transmission coil" : False. The transmission coil is used to create the magnetic field that is used to generate the MRI signal, but it does not play a direct role in spatial localization.

                Answer 3, "Varying magnetic field across the patient" : True. Spatial localization in MRI primarily relies on the fact that the magnetic field across the patient varies depending on where the signal is coming from. By manipulating the magnetic field, we can determine where in the body the signal is coming from.

                Answer 4, "Varying amplitude of RF pulse" : False. The amplitude of the RF pulse is used to control the amount of energy that is delivered to the body, but it does not play a direct role in spatial localization.

                Therefore, the correct answer is 3. "Varying magnetic field across the patient".

            Q :  
                There is a multiple choice question with 4 possible solutions. Here is the question : How to distinguish different frequencies in a signal?. Here is the answers : 1. "Using the known \(T_1\) value"  2. "With Fourier series"  3. "With Fourier transform"  4. "With Radon transform"  
            
            A : 
                To distinguish different frequencies in a signal, there are several methods available, but some are more relevant than others. 

                1. "Using the known \(T_1\) value": False. The \(T_1\) value is the is not related to the frequency components of a signal, it's simply the signal.

                2. "With Fourier series": partially True. Fourier series decomposition can be used to separate a signal into its frequency components. However, it is only applicable to periodic signals.

                3. "With Fourier transform": True. The Fourier transform is a mathematical tool that can be used to separate a signal into its frequency components. It works for both periodic and non-periodic signals.

                4. "With Radon transform": False. The Radon transform is a mathematical tool used in image processing to detect lines and curves in an image. It is not relevant for separating frequency components in a signal.

                Therefore, the correct answer is 3. "With Fourier transform".
            """
        elif(level == 4):
            ## we try few-shot prompting with different length
            self.instruction_prompt = """
            You are a teacher in an Institure of technology. Your goal is to provide correct and well explained answer so that your
            student can learn from your explaination. 

            Start by stating the definitions, lemmas, theorems, and formulas that are relevant to the resolution of the exercise.

            You'll have a question and multiple proposed answers. You will list all the answers in the order they were proposed. 
            For each of them you will you will proposed a reasoning justified by definitions and properties

            In a multiple choice question, a propostion is considered true when we can't find any counter example. It has to be true all the time.

            You will finish by simply stating what the answer was.

            Here's an example of interactions :

            Q : 
                There is a multiple choice question with 4 possible solutions. Here is the question : Spatial localization in MRI primarily relies on.... Here is the answers : 1. "Distance to the receiving coil"  2. "Distance from the transmission coil"  3. "Varying magnetic field across the patient"  4. "Varying amplitude of RF pulse"  

            A : 
                To answer this question, we need to understand how spatial localization works in MRI. Spatial localization in MRI refers to the ability to determine where in the body a specific signal is coming from. This is important because MRI scans provide detailed images of the inside of the body, so knowing where a signal is coming from allows us to create clear images of specific areas.

                Answer 1, "Distance to the receiving coil" : False. The distance to the receiving coil does not play a direct role in spatial localization. The receiving coil is used to detect the signal that is emitted by the body, but it does not determine where that signal is coming from.

                Answer 2, "Distance from the transmission coil" : False. The transmission coil is used to create the magnetic field that is used to generate the MRI signal, but it does not play a direct role in spatial localization.

                Answer 3, "Varying magnetic field across the patient" : True. Spatial localization in MRI primarily relies on the fact that the magnetic field across the patient varies depending on where the signal is coming from. By manipulating the magnetic field, we can determine where in the body the signal is coming from.

                Answer 4, "Varying amplitude of RF pulse" : False. The amplitude of the RF pulse is used to control the amount of energy that is delivered to the body, but it does not play a direct role in spatial localization.

                Therefore, the correct answer is 3. "Varying magnetic field across the patient".

            Q :  
                There is a multiple choice question with 4 possible solutions. Here is the question : How to distinguish different frequencies in a signal?. Here is the answers : 1. "Using the known \(T_1\) value"  2. "With Fourier series"  3. "With Fourier transform"  
            
            A : 
                To distinguish different frequencies in a signal, there are several methods available, but some are more relevant than others. 

                1. "Using the known \(T_1\) value": False. The \(T_1\) value is the is not related to the frequency components of a signal, it's simply the signal.

                2. "With Fourier series": partially True. Fourier series decomposition can be used to separate a signal into its frequency components. However, it is only applicable to periodic signals.

                3. "With Fourier transform": True. The Fourier transform is a mathematical tool that can be used to separate a signal into its frequency components. It works for both periodic and non-periodic signals.

                Therefore, the correct answer is 3. "With Fourier transform".


            Q : 
                There is a multiple choice question with 4 possible solutions. Here is the question : What is the goal of filterback projection?. Here is the answers : 1. "It helps to automatically remove artifacts and blurring"  2. "It reconstructs the images from helical to axial orientation"  
            
            A :
                To understand the goal of filterback projection, we need to first understand what it is. Filterback projection is a reconstruction technique used in computed tomography (CT) imaging to create a 2D or 3D image from a series of X-ray projections taken at different angles.

                1. "It helps to automatically remove artifacts and blurring": Partially true. While filterback projection can help to reduce artifacts and blurring in the reconstructed image, it does not do so automatically. The quality of the reconstructed image depends on several factors such as the accuracy of the projection data and the filter used.

                2. "It reconstructs the images from helical to axial orientation": False. The reconstruction of images from helical to axial orientation is a different technique that involves reformatting the raw data collected during a helical CT scan. Filterback projection is used to reconstruct images from the raw projection data.

                3. "It doubles the amount of scan data": False. Filterback projection does not increase the amount of scan data. It uses the available projection data to reconstruct the image.

                4. "It records data to compute the dose used for the scan": False. Filterback projection is a reconstruction technique and does not record data to compute the dose used for the scan. The dose used for the scan is determined by the X-ray tube and the scanning parameters used.

                Therefore, the correct answer is 1. "It helps to automatically remove artifacts and blurring" (with the clarification that it is not automatic).            
            """
    def get_budget(self):
        return Chat.budget()

    def queryMCQ(self, sample):
        chat = Chat.create(f"chat TEST {self.session_id}")
        self.session_id += 1

        answers = ' '.join([f"""{i+1}. "{answer}" """ for i, answer in enumerate(sample['choices'])])
        form_question = f"""There is a multiple choice question with {len(sample['choices'])} possible solutions. Here is the question : {sample['question']}. Here is the answers : {answers} """
        message = chat.ask(form_question,
                   instruction=self.instruction_prompt)
    
        return form_question, message
    
    
    def querySimple(self, sample):
        chat = Chat.create(f"chat TEST {self.session_id}")
        self.session_id += 1
        
        form_question = f"""Here is the question : {sample['question']}"""
        message = chat.ask(form_question,
                    instruction=self.prompt_simpleQ)
        return form_question, message
    
    def display(self, sample, form_question, answer):
        print(f"##########  {self.session_id}  ##########")
        print(sample['question'])
        print("##############################")
        print(form_question)
        print("##############################")
        print(answer)
        print("#########################")

    def query_and_display(self, sample):
        if('choices' in sample.keys()):

            if(sample['choices'] == ["Yes", "No"]):
                query_func = self.querySimple
            ## mcq question
            query_func = self.queryMCQ
        else:
            ## simple question
            query_func = self.querySimple
        form_question, answer = query_func(sample)
        self.display(sample, form_question, answer)
        
    def query_all(self, data):
        answered_queries = []
        for sample in tqdm(data, desc="Processing samples"):
            ## determine which query function
            if('choices' in sample.keys()):

                if(sample['choices'] == ["Yes", "No"]):
                    query_func = self.querySimple
                ## mcq question
                query_func = self.queryMCQ
            else:
                ## simple question
                query_func = self.querySimple
            
            ## make query
            form_question, answer = query_func(sample)

            sample["answer"] = answer
            sample["form_question"] = form_question

            answered_queries.append(sample)
        return answered_queries





    
    