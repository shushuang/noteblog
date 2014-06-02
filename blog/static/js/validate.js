function validate_required(val)
{
	if(val.trim() != '')
	{
		return true;
	}
	else
	{
		return false;
	}
}
function validate_alphanum(val)
{
	reg = /^[a-zA-Z0-9]+$/;
	if(reg.test(val))
	{
		return true;
	}
	else
	{
		return false;
	}
}
function validate_email(val)
{
	reg = /^[a-zA-Z0-9]+@[a-zA-Z0-9.]+$/;
	if(reg.test(val))
	{
		return true;
	}
	else
	{
		return false;
	}
}