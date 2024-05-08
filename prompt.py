'''
You might be inclined to think that prompting an LLM shouldn't be that hard;
after all, it's just about describing your requirements to the model in 
natural language, right? In practice, it isn't as straightforward. 
Some might better adhere to your desired output format, while 
others may necessitate more detailed instructions. The task you
wish the LLM to perform could be complex, requiring elaborate 
and precise instructions. Therefore, devising a suitable prompt 
often entails a lot of experimentation and benchmarking.
'''

def story_telling():
  return  """
  {context}
  System Note: the story slowly and elaborate on every given detail. in about 20 statements .
  Story Goal: {question}
  """

def instructional_scenario():
  return  """
  {context}
  System Note: create a pedagogical scenario based on teacher question use real world probleme to construct
  activities for students and use the probleme solving method to construct teaching materials (define,prepare,
  try,reflect) and give the instructional scenario as a latex template as shown below.
  example of output:
  \\begin table [h]
  \\centering
  \\begin tabular |c|c|c|c|c|c| 
  \\hline
  Learning Objectives & Competences & Time & Teacher Role & Student Role & Activity \\\\
  \\hline
  learning_objectives & competences & time  & teacher_role & student_role & activity \\\\
  \\hline
  \\end tabular 
  \\end able
  {question}
  """