# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import StickyNote
from .forms import StickyNoteForm

def stickynote_list(request):
    stickynotes = StickyNote.objects.filter(created_by=request.user)
    return render(request, 'stickynote_list.html', {'stickynotes': stickynotes})

def stickynote_detail(request, pk):
    stickynote = get_object_or_404(StickyNote, pk=pk, created_by=request.user)
    return render(request, 'stickynote_detail.html', {'stickynote': stickynote})

def stickynote_create(request):
    if request.method == 'POST':
        form = StickyNoteForm(request.POST)
        if form.is_valid():
            stickynote = form.save(commit=False)
            stickynote.created_by = request.user
            stickynote.save()
            return redirect('stickynote_list')
    else:
        form = StickyNoteForm()
    return render(request, 'stickynote_form.html', {'form': form})

def stickynote_update(request, pk):
    stickynote = get_object_or_404(StickyNote, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = StickyNoteForm(request.POST, instance=stickynote)
        if form.is_valid():
            form.save()
            return redirect('stickynote_list')
    else:
        form = StickyNoteForm(instance=stickynote)
    return render(request, 'stickynote_form.html', {'form': form})

def stickynote_delete(request, pk):
    stickynote = get_object_or_404(StickyNote, pk=pk, created_by=request.user)
    if request.method == 'POST':
        stickynote.delete()
        return redirect('stickynote_list')
    return render(request, 'stickynote_confirm_delete.html', {'stickynote': stickynote})
