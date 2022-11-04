import operator
class Shortcode():
	def __init__(self,Unprompted):
		self.Unprompted = Unprompted
		self.ops = {"==":self.Unprompted.is_equal,"<":operator.lt,"<=":operator.le,">":operator.gt,">=":operator.ge}
	def run_block(self, pargs, kwargs, context, content):
		_not = "_not" in pargs
		_any = "_any" in pargs

		is_true = not _any

		_op = kwargs["_operator"] if "_operator" in kwargs else "=="
		
		for key, value in kwargs.items():
			if (key[0] == "_"): continue # Skips system arguments

			this_value = self.Unprompted.parse_alt_tags(value,context)
			
			# Fix data type
			if (_op != "=="):
				self.Unprompted.shortcode_user_vars[key] = float(self.Unprompted.shortcode_user_vars[key])
				this_value = float(this_value)
			
			if (self.ops[_op](self.Unprompted.shortcode_user_vars[key],this_value)):
				if _any:
					is_true = True
					break
			elif not _any:
				is_true = False
				break

		if ((is_true and not _not) or (_not and not is_true)):
			self.Unprompted.shortcode_objects["else"].do_else = False
			return(self.Unprompted.parse_alt_tags(content,context))
		else:
			self.Unprompted.shortcode_objects["else"].do_else = True
			return("")