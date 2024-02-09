from django.shortcuts import render, redirect
from .models import Note
from .forms import NoteForm
from django.contrib.auth.decorators import login_required


@login_required()
def note_list(request):
    notes = Note.objects.filter(user=request.user)
    return render(request, 'notes/noteList.html', {'notes': notes})


@login_required()
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/createNote.html', {'form': form})


@login_required()
def update_note(request, pk):
    try:
        note = Note.objects.fiter(user=request.user).get(pk=pk)
        form = NoteForm(instance=note)
        if request.method == 'POST':
            form = NoteForm(request.POST, instance=note)
            if form.is_valid():
                form.save()
                redirect('note_list')
    except Note.DoesNotExist:
        return redirect('note_list')
    return render(request, 'notes/createNote.html', {'form': form})


@login_required()
def delete_note(request, pk):
    note = Note.objects.filter(user=request.user).get(pk=pk)
    note.delete()
    return redirect('note_list')
